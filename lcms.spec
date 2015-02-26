#
# Conditional build:
%bcond_without	python	# don't build python bindings
#
Summary:	Little CMS - a library to transform between colour profiles
Summary(pl.UTF-8):	Little CMS - biblioteka do konwersji między profilami kolorów
Name:		lcms
Version:	1.19
Release:	4
License:	MIT
Group:		Libraries
Source0:	http://downloads.sourceforge.net/lcms/%{name}-%{version}.tar.gz
# Source0-md5:	8af94611baf20d9646c7c2c285859818
Patch0:		%{name}-python.patch
URL:		http://www.littlecms.com/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.7.2
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	sed >= 4.0
%if %{with python}
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	swig-python >= 1.3.30
%endif
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Little CMS intends to be a small-footprint color management engine,
with special focus on accuracy and performance. It uses the
International Color Consortium standard (ICC), which is the modern
standard when regarding to color management.

Little CMS 1.x supports ICC profile specification v3.4.

%description -l pl.UTF-8
Little CMS jest lekkim silnikiem zarządzania kolorami, tworzonym
przede wszystkim z myślą o dokładności i wydajności. Wykorzystuje
standard International Color Consortium (ICC), będący współczesnym
standardem zarządzania kolorami.

Little CMS 1.x obsługuje specyfikację profili ICC w wersji 3.4.

%package devel
Summary:	Little CMS - header files and developer's documentation
Summary(pl.UTF-8):	Little CMS - pliki nagłówkowe i dokumentacja
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files needed to compile programs with liblcms and some
documentation useful for programmers.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do konsolidacji z liblcms oraz dokumentacja
dla programistów.

%package static
Summary:	Little CMS - static library
Summary(pl.UTF-8):	Little CMS - biblioteka statyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of liblcms.

%description static -l pl.UTF-8
Statyczna biblioteka liblcms.

%package progs
Summary:	Example and demonstration programs for Little CMS
Summary(pl.UTF-8):	Programy przykładowe i demonstracyjne do Little CMS
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description progs
Example and demonstration programs for Little CMS.

%description progs -l pl.UTF-8
Programy przykładowe i demonstracyjne do Little CMS.

%package -n python-lcms
Summary:	Little CMS module for Python
Summary(pl.UTF-8):	Moduł Little CMS dla Pythona
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python

%description -n python-lcms
Little CMS module for Python.

%description -n python-lcms -l pl.UTF-8
Moduł Little CMS dla Pythona.

%prep
%setup -q
%undos configure.ac
%patch0 -p1

%build
# rebuild using newer swig (needed for g++ 4/python 2.5)
cd python
rm -f lcms.py lcms_wrap.cxx
swig -python -c++ -I../include lcms.i
cd ..
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with%{!?with_python:out}-python

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install samples/{icctrans,wtpt} tifficc/tifficc $RPM_BUILD_ROOT%{_bindir}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.1ST
%attr(755,root,root) %{_libdir}/liblcms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblcms.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/liblcms.so
%{_libdir}/liblcms.la
%{_includedir}/icc34.h
%{_includedir}/lcms.h
%{_pkgconfigdir}/lcms.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblcms.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/icc2ps
%attr(755,root,root) %{_bindir}/icclink
%attr(755,root,root) %{_bindir}/icctrans
%attr(755,root,root) %{_bindir}/jpegicc
%attr(755,root,root) %{_bindir}/tiffdiff
%attr(755,root,root) %{_bindir}/tifficc
%attr(755,root,root) %{_bindir}/wtpt
%{_mandir}/man1/icc2ps.1*
%{_mandir}/man1/icclink.1*
%{_mandir}/man1/jpegicc.1*
%{_mandir}/man1/tifficc.1*
%{_mandir}/man1/wtpt.1*

%if %{with python}
%files -n python-lcms
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_lcms.so
%{py_sitedir}/lcms.py
%endif
