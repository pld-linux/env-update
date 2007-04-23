Summary:	env-update - create /etc/profile.env from /etc/env.d files
Summary(pl.UTF-8):	env-update - tworzenie /etc/profile.env z plików /etc/env.d
Name:		env-update
Version:	1.6.15
Release:	1
License:	GPL v2
Group:		Base
Source0:	http://distfiles.gentoo.org/distfiles/rc-scripts-%{version}.tar.bz2
# Source0-md5:	e3dd64c9b45454a99ce51ee2ec4b1fd5
Patch0:		%{name}.patch
Patch1:		%{name}-cflags.patch
BuildRequires:	gawk-devel
BuildRequires:	rpmbuild(macros) >= 1.316
Requires:	gawk
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_libdir		/lib
%define		_libexecdir	/lib
%define		_sbindir	/sbin

%description
This is env-update rip from gentoo's baselayout.

env-update creates /etc/profile.env and /etc/csh.env from the contents
of /etc/env.d/, so your shell is able to read initial env quickly even
at high system loads.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzie env-update wyciągnięte z podstawowych
narzędzi gentoo.

env-update tworzy plik /etc/profile.env z plików /etc/env.d, dzięki
czemu powłoka jest w stanie szybko wczytać początkowe środowisko nawet
przy dużym obciążeniu systemu.

%prep
%setup -q -n rc-scripts-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__make} -C src/filefuncs \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LD="%{__ld}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_libexecdir},%{_sbindir},%{_sysconfdir},/var/cache}
install src/filefuncs/filefuncs.so $RPM_BUILD_ROOT%{_libdir}
install -p src/awk/{functions.awk,genenviron.awk} $RPM_BUILD_ROOT%{_libexecdir}
install sbin/env-update.sh $RPM_BUILD_ROOT%{_sbindir}/env-update
touch $RPM_BUILD_ROOT/var/cache/envcache
touch $RPM_BUILD_ROOT%{_sysconfdir}/{profile,csh}.env

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/env-update

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/filefuncs.so
%{_libexecdir}/*.awk
%ghost /var/cache/envcache
%ghost %{_sysconfdir}/profile.env
%ghost %{_sysconfdir}/csh.env
