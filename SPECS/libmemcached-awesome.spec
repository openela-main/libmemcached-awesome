# Spec file for libmemcached-awesome from
#
# remirepo spec file for libmemcached-awesome
#
# Copyright (c) 2009-2021 Remi Collet
# License: CC-BY-SA
# https://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without               tests

%global libname              libmemcached

%global gh_commit            0ff88be3322a493773956028d4022d995f3cb193
%global gh_short             %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner             awesomized
%global gh_project           libmemcached

%global upstream_version     1.1.0
#global upstream_prever      beta3

Name:      %{libname}-awesome
Summary:   Client library and command line tools for memcached server
Version:   %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:   12%{?dist}
License:   BSD
URL:       https://github.com/%{gh_owner}/%{gh_project}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

Patch0:    %{name}-catch.patch
Patch1:    %{name}-aes.patch
Patch2:    %{name}-config.patch
Patch3:    %{name}-macro.patch
Patch4:    %{name}-testing.patch
Patch5:    %{name}-udp-test.patch
# rhbz#1995795
Patch6:	   %{name}-aes2.patch
Patch7:    %{name}-rpath.patch

BuildRequires: cmake >= 3.9
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: python3-sphinx
BuildRequires: cyrus-sasl-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: memcached
BuildRequires: systemtap-sdt-devel
BuildRequires: libevent-devel > 2
BuildRequires: openssl-devel

Provides:      bundled(bobjenkins-hash)
# package rename
Obsoletes:     %{libname}-libs         < 1.1
Provides:      %{libname}-libs         = %{version}-%{release}
Provides:      %{libname}-libs%{?_isa} = %{version}-%{release}


%description
%{name} is a C/C++ client library and tools for the memcached
server (https://memcached.org/). It has been designed to be light
on memory usage, and provide full access to server side methods.

This is a resurrection of the original work from Brian Aker at libmemcached.org.


%package devel
Summary:    Header files and development libraries for %{name}

Requires:   %{name}%{?_isa} = %{version}-%{release}
# package rename
Obsoletes:  %{libname}-devel         < 1.1
Provides:   %{libname}-devel         = %{version}-%{release}
Provides:   %{libname}-devel%{?_isa} = %{version}-%{release}
Requires:   cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

Documentation: https://awesomized.github.io/libmemcached


%package tools
Summary:    %{name} tools

Requires:   %{name}%{?_isa} = %{version}-%{release}
# package rename
Obsoletes:  %{libname}         < 1.1
Provides:   %{libname}         = %{version}-%{release}
Provides:   %{libname}%{?_isa} = %{version}-%{release}

%description tools
This package contains the %{libname}-awesome command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# drop test hanging in mock
# and requiring some memcached build options
rm test/tests/memcached/sasl.cpp
# temporarily ignore wuth erratic failure
%ifarch s390x
rm test/tests/memcached/udp.cpp
%endif


%build
%set_build_flags
LDFLAGS="${LDFLAGS} -Wl,--enable-new-dtags"
%cmake \
  -DBUILD_TESTING:BOOL=ON \
  -DBUILD_DOCS_MAN:BOOL=ON \
  -DBUILD_DOCS_MANGZ:BOOL=OFF \
  -DENABLE_SASL:BOOL=ON \
  -DENABLE_DTRACE:BOOL=ON \
  -DENABLE_OPENSSL_CRYPTO:BOOL=ON \
  -DENABLE_HASH_HSIEH:BOOL=ON \
  -DENABLE_HASH_FNV64:BOOL=ON \
  -DENABLE_HASH_MURMUR:BOOL=ON \
  -DENABLE_MEMASLAP:BOOL=ON

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_datadir}/%{name}/example.cnf support

rm -r %{buildroot}%{_datadir}/doc/%{name}/


%check
%if %{with tests}
: Run test suite
%ctest
%else
: Skip test suite
%endif


%files tools
%{_bindir}/mem*
%{_mandir}/man1/mem*

%files
%license LICENSE
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*

%files devel
%doc example
%doc *.md
%doc AUTHORS
%doc support/example.cnf
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_libdir}/cmake/%{name}
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*


%changelog
* Fri Nov 12 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-12
- Fix rpath
- Related: rhbz#1995795

* Fri Nov 12 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-11
- Add flag to linker flags
- Related: rhbz#1995795

* Thu Nov 11 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-10
- Remove aes implementation from the sources completely
- Resolves: rhbz#1995795

* Fri Aug 06 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-9
- Disable unstable test for udp
- Related: rhbz#1981785

* Fri Aug 06 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-8
- Add requires cyrus-sasl-devel to devel subpackage
- Related: rhbz#1981785

* Mon Aug 02 2021 Tomas Korbar <tkorbar@redhat.com> - 1.1.0-7
- Remove unstable test
- Related: rhbz#1981785

* Tue Jul 27 2021 Remi Collet <remi@remirepo.net> - 1.1.0-6
- add LIBMEMCACHED_AWESOME macro from
  https://github.com/awesomized/libmemcached/pull/115

* Mon Jul 26 2021 Remi Collet <remi@remirepo.net> - 1.1.0-5
- fix missing HAVE_SSIZE_T macro using patch from
  https://github.com/awesomized/libmemcached/pull/117

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 1.1.0-3
- use upstream patch for libcrypto

* Fri Jun 25 2021 Remi Collet <remi@remirepo.net> - 1.1.0-2
- remove internal AES implementation and use libcrypto
  https://github.com/awesomized/libmemcached/pull/114
- fix build ussing upstream patch to update catch version

* Thu Jun 24 2021 Remi Collet <remi@remirepo.net> - 1.1.0-1
- Initial RPM from libmemcached-awesome
  from old libmemcached spec file
