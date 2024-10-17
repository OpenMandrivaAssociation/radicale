%define oname	Radicale

%define _radicaledir %{_localstatedir}/lib/%{name}

Summary:	Simple calendar server
Name:		radicale
Version:	0.7.1
Release:	4
Source0:	http://radicale.org/src/%{name}/%{oname}-%{version}.tar.gz
Source1:	radicale.service
Source2:	README.urpmi
Patch0:		Radicale-0.7-config.patch
Group:		Office
License:	GPLv3+
URL:		https://radicale.org/
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
install -Dm0755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README config.default README.urpmi
%{_bindir}/%{name}
%{_unitdir}/%{name}.service 
%{_radicaledir}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/users
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{oname}-%{version}-py%{py_ver}.egg-info
