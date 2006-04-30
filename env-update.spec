Summary:	env-update - create /etc/profile.env from /etc/env.d files
Summary(pl):	env-update - tworzenie /etc/profile.env z plików /etc/env.d
Name:		env-update
Version:	1.6.14
Release:	0.6
License:	GPL v2
Group:		Base
Source0:	http://distfiles.gentoo.org/distfiles/rc-scripts-%{version}.tar.bz2
# Source0-md5:	3ef9ae479847d474c33d7d54f4912e77
Patch0:		%{name}.patch
Patch1:		%{name}-cflags.patch
BuildRequires:	gawk-devel
Requires:	gawk
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/

%description
This is env-update rip from gentoo's baselayout.

env-update creates /etc/profile.env file from /etc/env.d files, so
your shell is able to read initial env quickly even at high system
loads.

%description -l pl
Ten pakiet zawiera narzêdzie env-update wyci±gniête z podstawowych
narzêdzi gentoo.

env-update tworzy plik /etc/profile.env z plików /etc/env.d, dziêki
czemu pow³oka jest w stanie szybko wczytaæ pocz±tkowe ¶rodowisko nawet
przy du¿ym obci±¿eniu systemu.

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
install -d $RPM_BUILD_ROOT{%{_libdir},%{_libexecdir},%{_sbindir},/var/cache}
install src/filefuncs/filefuncs.so $RPM_BUILD_ROOT%{_libdir}
install -p src/awk/{functions.awk,genenviron.awk} $RPM_BUILD_ROOT%{_libexecdir}
install sbin/env-update.sh $RPM_BUILD_ROOT%{_sbindir}/env-update
touch $RPM_BUILD_ROOT/var/cache/envcache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/filefuncs.so
%{_libexecdir}/*.awk
%ghost /var/cache/envcache
