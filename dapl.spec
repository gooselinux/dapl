Name: dapl
Version: 2.0.25
Release: 5%{?dist}
Summary: Library providing access to the DAT 2.0 API
Group: System Environment/Libraries
License: GPLv2 or BSD or CPL
Url: http://openfabrics.org/
Source0: http://www.openfabrics.org/downloads/dapl/dapl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes: udapl < 1.3
BuildRequires: libibverbs-devel >= 1.1.3, librdmacm-devel >= 1.0.10
BuildRequires: autoconf, libtool
ExclusiveArch: i386 x86_64 ia64 ppc ppc64
%description
libdat and libdapl provide a userspace implementation of the DAT 2.0
API and is built to natively support InfiniBand/iWARP network technology.

%package devel
Summary: Development files for the libdat and libdapl libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: udapl-devel < 1.3
%description devel
Header files for libdat and libdapl library.

%package static
Summary: Static libdat and libdapl libraries
Group: System Environment/Libraries
Requires: %{name}-devel = %{version}-%{release}
Obsoletes: dapl-devel-static < 2.0.24
%description static
Static versions of the libdat and libdapl libraries.

%package utils
Summary: Test suites for dapl libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%description utils
Useful test suites to validate the dapl library API's and operation.

%prep
%setup -q
aclocal -I config && libtoolize --force --copy && autoheader && \
    automake --foreign --add-missing --copy && autoconf

%build
%configure CFLAGS="$CFLAGS -fno-strict-aliasing" --enable-ext-type=ib --sysconfdir=/etc/rdma
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/rdma/dat.conf
%doc AUTHORS README ChangeLog COPYING

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%dir %{_includedir}/dat2
%{_includedir}/dat2/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Mar 07 2010 Doug Ledford <dledford@redhat.com> - 2.0.25-5.el6
- I missed that the license was in an invalid form, correct that
- Related: bz555835

* Sun Mar 07 2010 Doug Ledford <dledford@redhat.com> - 2.0.25-4.el6
- Clean up rpmlint warnings about unversioned obsoletes
- Make setup quite
- Include COPYING file in docs
- Fix naked macro in changelog
- Related: bz555835

* Thu Jan 21 2010 Doug Ledford <dledford@redhat.com> - 2.0.25-3.el6
- Update config directory for rhel6 (from /etc/ofed to /etc/rdma)
- Remove compat-dapl and split it off to its own rpm
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 2.0.25-2.el5
- Fix up file lists for upstream binary name changes

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 2.0.25-1.el5
- Update to latest upstream version
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 2.0.19-2
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Fri Jun 19 2009 Doug Ledford <dledford@redhat.com> - 2.0.19-1
- Recompile against non-XRC libibverbs
- Update to OFED 1.4.1 final bits
- Related: bz506258, bz506097

* Fri Apr 24 2009 Doug Ledford <dledford@redhat.com> - 2.0.17-2
- Add -fno-strict-aliasing to CFLAGS

* Thu Apr 16 2009 Doug Ledford <dledford@redhat.com> - 2.0.17-1
- Move the dat-1.2 conf file to /etc/ofed/compat-dapl/dat.conf
- Update to ofed 1.4.1-rc3 versions of dapl
- Related: bz459652

* Thu Oct 16 2008 Doug Ledford <dledford@redhat.com> - 2.0.13-4
- Import the upstream fix for bug 465840
- Related: bz465840

* Mon Oct 13 2008 Doug Ledford <dledford@redhat.com> - 2.0.13-3
- Add a compat-dapl-utils package so people can test their dapl-1.2
  setups
- Even though we tell dapl to look for its config in /etc/ofed, it wasn't
  actually looking there.  Fix that.
- Resolves: bz465841, bz465840

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 2.0.13-2
- I don't know what I was thinking putting the version into the compat
  dapl packages names...makes upgrades not work and makes things like
  buildrequire compat-dapl-devel not work.  Removed, and we now obsolete
  the existing compat-dapl*-{version} packages.

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 2.0.13-1
- Update to latest upstream versions for both dapl and compat-dapl
- Resolves: bz451468

* Thu Apr 03 2008 Doug Ledford <dledford@redhat.com> - 2.0.7-2
- Need a new brew build in order to get the filelist correct in the errata
- Related: bz428197

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 2.0.7-1
- Update to same dapl versions as OFED 1.3 final bits
- Upstream modified dapl-1.2 and dapl-2.0 to coexist, so undo the changes we
  made in order for them to coexist in our package
- Related: bz428197

* Tue Jan 29 2008 Doug Ledford <dledford@redhat.com> - 2.0.3-3
- Make dapl-1.2 and dapl-2.0 devel environments coexist, and make dapl-1.2
  the default lib so that unported apps continue to build, and ported apps
  build properly by adding -L%%{_libdir}/dat -ldat to their LDFLAGS.

* Tue Jan 15 2008 Doug Ledford <dledford@redhat.com> - 2.0.3-2
- Import upstream package, gut spec file, copy over dapl spec from openib spec
- Merge dapl 1.2 and 2.0 support into a single rpm
- Related: bz428197

* Tue Nov 20 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.3
- DAT/DAPL Version 2.0.3 Release 1

* Tue Oct 30 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.2
- DAT/DAPL Version 2.0.2 Release 1

* Tue Sep 18 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.1-1
- OFED 1.3-alpha, co-exist with DAT 1.2 library package.  

* Wed Mar 7 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.0.pre
- Initial release of DAT 2.0 APIs, includes IB extensions 
