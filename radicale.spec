# TODO:
# -improve init file

%define oname	Radicale
%define name	radicale

%define _radicaledir %{_localstatedir}/lib/%{name}

Summary:	Simple calendar server
Name:		%{name}
Version:	0.7.1
Release:	1
Source0:	http://radicale.org/src/%{name}/%{oname}-%{version}.tar.gz
Source1:	radicale.init
Source2:	README.urpmi
Patch0:		Radicale-0.7-config.patch
Group:		Office
License:	GPLv3+
URL:		http://radicale.org/
BuildArch:	noarch
BuildRequires:	python-devel
Requires(pre):		rpm-helper
Requires(preun):	rpm-helper
Obsoletes:	python-%{name}
Suggests:	python-OpenSSL

%description
The Radicale Project is a complete CalDAV calendar server solution. It can
store multiple calendars.

Calendars are available from both local and distant accesses, possibly
limited through authentication policies.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -b .default

#README.urpmi
cp %{SOURCE2} .

%build
#nothing to do

%install
python setup.py install --root=%{buildroot}

#dir for calendars
install -dm0755 %{buildroot}%{_radicaledir}/calendars

#config
install -Dm0644 config %{buildroot}%{_sysconfdir}/%{name}/config

#Empty htpasswd file
echo "# Htpasswd file for Radical" > %{buildroot}%{_sysconfdir}/%{name}/users

#init
install -Dm0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc README config.default README.urpmi
%{_bindir}/%{name}
%{_initrddir}/%{name} 
%{_radicaledir}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/users
%{python_sitelib}/%{name}
%{python_sitelib}/%{oname}-%{version}-py%{py_ver}.egg-info


%changelog
* Wed Jun 01 2011 Jani Välimaa <wally@mandriva.org> 0.5-2mdv2011.0
+ Revision: 682370
- rebuild to obsolete old pkgs

* Sun Apr 10 2011 Jani Välimaa <wally@mandriva.org> 0.5-1
+ Revision: 652344
- new version 0.5
- merge python parts to main package
- obsolete old python subpackage
- add python-devel BR

* Sun Dec 19 2010 Jani Välimaa <wally@mandriva.org> 0.4-3mdv2011.0
+ Revision: 623156
- create dir for calendars

* Fri Dec 17 2010 Jani Välimaa <wally@mandriva.org> 0.4-2mdv2011.0
+ Revision: 622753
- fix typos in a several places
- fix description in init file

* Fri Dec 17 2010 Jani Välimaa <wally@mandriva.org> 0.4-1mdv2011.0
+ Revision: 622738
- import radicale

