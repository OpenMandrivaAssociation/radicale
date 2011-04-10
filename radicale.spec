# TODO:
# -improve init file

%define oname	Radicale
%define name	radicale
%define version	0.5
%define rel	1

%define _radicaledir %{_localstatedir}/lib/%{name}

Summary:	Simple calendar server
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Source0:	http://radicale.org/src/%{name}/%{oname}-%{version}.tar.gz
Source1:	radicale.init
Source2:	README.urpmi
Patch0:		Radicale-0.4-config.patch
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
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc NEWS README TODO config.default README.urpmi
%{_bindir}/%{name}
%{_initrddir}/%{name} 
%{_radicaledir}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/users
%{python_sitelib}/%{name}
%{python_sitelib}/%{oname}-%{version}-py%{pyver}.egg-info
