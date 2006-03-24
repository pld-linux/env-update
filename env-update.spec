Summary:	env-update
Name:		env-update
Version:	1.6.14
Release:	0.2
License:	GPL v2
Group:		Base
Source0:	http://distfiles.gentoo.org/distfiles/rc-scripts-%{version}.tar.bz2
# Source0-md5:	3ef9ae479847d474c33d7d54f4912e77
Patch0:		%{name}.patch
BuildRequires:	gawk-devel
Requires:	gawk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is env-update rip from gentoo's baselayout.

env-update creates /etc/profile.env file from /etc/env.d files, so
your shell is able to read initial env quickly even at high system
loads.

%prep
%setup -q -n rc-scripts-%{version}
%patch0 -p1

%build
%{__make} -C src/filefuncs \
	CC="%{__cc}" \
	LD="%{__ld}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_libexecdir},%{_sbindir}}
install src/filefuncs/filefuncs.so $RPM_BUILD_ROOT%{_libdir}
install -p src/awk/{functions.awk,genenviron.awk} $RPM_BUILD_ROOT%{_libexecdir}
install sbin/env-update.sh $RPM_BUILD_ROOT%{_sbindir}/env-update

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/filefuncs.so
%{_libexecdir}/*.awk
