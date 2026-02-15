Summary:	An unofficial CLI OneDrive Client for Linux
Name:	onedrive
Version:	2.5.10
Release:	1
Group:	Networking/Other
License:	GPLv3+
Url:		https://github.com/abraunegg/%{name}
Source0:	https://github.com/abraunegg/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:	onedrive-2.5.10-fix-websocket-trigger-not-syncing.patch
Patch1:	onedrive-2.5.10-fix-internal-crash-if-websocket-init-fails.patch
BuildRequires:	chrpath
BuildRequires:	ldc
BuildRequires:	qt6-qttools-assistant
BuildRequires:	systemd
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(sqlite3)
Requires(preun): systemd
Requires:	logrotate

%description
A free Microsoft OneDrive Client which supports OneDrive Personal,
OneDrive for Business, OneDrive for Office365 and SharePoint.
This powerful and highly configurable client can run on all major Linux
distributions, FreeBSD, or as a Docker container. It supports one-way
and two-way sync capabilities and securely connects to Microsoft
OneDrive services.
NOTE: OneDrive is not a free software based service.

%files
%license LICENSE
%doc readme.md changelog.md
%doc docs/*
%config %{_sysconfdir}/logrotate.d/%{name}
%ghost %attr(0755,root,root) %dir %{_var}/log/%{name}
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_datadir}/bash-completion/completions/%{name}
%{_iconsdir}/hicolor/scalable/places/%{name}.svg
%{_mandir}/man1/%{name}.1*

%preun
%systemd_user_preun %{name}.service
%systemd_preun %{name}@.service

#---------------------------------------------------------------------------

%prep
%autosetup -p1


%build
%configure \
	--enable-notifications \
	--enable-completions \
	--with-systemduserunitdir=%{_userunitdir} \
	--with-systemdsystemunitdir=%{_unitdir}

export DFLAGS="-O -g -release -v -wi"
%make_build DC=ldmd2


%install
%make_install

# Remove automatic doc files
rm -fr %{buildroot}%{_docdir}

# Fix rpath error
chrpath -d %{buildroot}%{_bindir}/%{name}

# Drop fish and zsh completions (in the wrong spot)
rm -rf %{buildroot}/usr/local/*
