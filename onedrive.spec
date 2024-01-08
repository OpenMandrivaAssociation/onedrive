Summary:	An unofficial CLI OneDrive Client for Linux
Name:		onedrive
Version:	2.4.25
Release:	1
Group:		Networking/Other
License:	GPLv3
URL:		https://github.com/abraunegg/%{name}
Source0:	https://github.com/abraunegg/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
BuildRequires:	ldc
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	systemd
Requires(preun): systemd
Requires:	logrotate

%description
#--------------------------------------------------------------------
A free Microsoft OneDrive Client which supports OneDrive Personal,
OneDrive for Business, OneDrive for Office365 and SharePoint.

This powerful and highly configurable client can run on all major Linux
distributions, FreeBSD, or as a Docker container. It supports one-way
and two-way sync capabilities and securely connects to Microsoft
OneDrive services.

NOTE: OneDrive is not a free software based service.

%files
%license LICENSE
%doc README.md CHANGELOG.md
%doc docs/BusinessSharedFolders.md
%doc docs/Docker.md
%doc docs/INSTALL.md
%doc docs/SharePoint-Shared-Libraries.md
%doc docs/USAGE.md
%doc docs/advanced-usage.md
%doc docs/application-security.md
%doc config
%{_bindir}/%{name}
%config %{_sysconfdir}/logrotate.d/onedrive
%{_userunitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_mandir}/man1/%{name}.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%configure \
	--with-systemduserunitdir=%{_userunitdir} \
	--with-systemdsystemunitdir=%{_unitdir}
export DFLAGS="-O -g -release -v -wi"
%make_build DC=ldmd2

%install
%make_install

# remove automatic doc files
rm -fr %{buildroot}/%{_docdir}

%preun
%systemd_user_preun %{name}.service
%systemd_preun %{name}@.service

