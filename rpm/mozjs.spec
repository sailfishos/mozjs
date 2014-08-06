Name:       mozjs

%define package_name_simple js
%define package_version_major 17
%define package_version_major_minor 17.0

Summary:    SpiderMonkey JavaScript Engine
Version:    17.0.0
Release:    1
Group:      System/Libraries
License:    MPL2
URL:        https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source:     %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  python

%description
SpiderMonkey is Mozilla's JavaScript engine written in C/C++.

%package devel
Summary:    Development files for SpiderMonkey
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(nspr)

%description devel
Development files for SpiderMonkey.

%package bin
Summary:    Command-line JavaScript interpreter
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description bin
JavaScript interpreter from SpiderMonkey.

%prep
%setup -q -n %{name}-%{version}

%build
cd %{name}/js/src

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd %{name}/js/src
%make_install

# Fix permissions of files of devel package
find %{buildroot}/%{_includedir} -type f -exec chmod 644 {} +
find %{buildroot}/%{_libdir}/pkgconfig -type f -exec chmod 644 {} +

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-%{package_version_major_minor}.so

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{package_name_simple}%{package_version_major}-config
%{_includedir}/%{package_name_simple}-%{package_version_major_minor}
%{_libdir}/pkgconfig/%{name}-%{package_version_major_minor}.pc

%files bin
%defattr(-,root,root,-)
%{_bindir}/%{package_name_simple}%{package_version_major}
