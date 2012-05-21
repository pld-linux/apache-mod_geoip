%define		mod_name	geoip
%define 	apxs		%{_sbindir}/apxs
Summary:	GeoIP module for the Apache HTTP Server
Name:		apache-mod_%{mod_name}
Version:	1.2.7
Release:	1
License:	ASL 1.1
Group:		Daemons
URL:		https://www.maxmind.com/app/mod_geoip
Source0:	http://www.maxmind.com/download/geoip/api/mod_geoip2/mod_%{mod_name}2_%{version}.tar.gz
# Source0-md5:	76514ad0e8adb8cd8231c5e3646d03fd
Source1:	apache.conf
BuildRequires:	%{apxs}
BuildRequires:	GeoIP-devel >= 1.4.8
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Suggests:	GeoIP-db-City
Suggests:	GeoIP-db-Country
Suggests:	GeoIP-db-IPASNum
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_geoip is an Apache module for finding the country that a web
request originated from. It uses the GeoIP library and database to
perform the lookup. It is free software, licensed under the Apache
license.

%prep
%setup -q -n mod_geoip2_%{version}

%build
%{apxs} -Wc,"%{rpmcppflags} %{rpmcflags}" -Wl,"-lGeoIP %{rpmldflags}" -c mod_geoip.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -Dp .libs/mod_geoip.so $RPM_BUILD_ROOT%{_pkglibdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi


%files
%defattr(644,root,root,755)
%doc INSTALL README* Changes
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
