#
# Conditional build:
%bcond_without	qt	# without Qt GUI
%bcond_without	x11	# without X11 session monitoring

Summary:	Desktop full-text search tool
Name:		recoll
Version:	1.28.5
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://www.lesbonscomptes.com/recoll/%{name}-%{version}.tar.gz
# Source0-md5:	95220f5bd221f262fd7246ae82b4136d
URL:		https://www.lesbonscomptes.com/recoll/
BuildRequires:	aspell-devel
BuildRequires:	chmlib-devel
BuildRequires:	libxslt-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	xapian-core-devel
%{?with_x11:BuildRequires:	xorg-lib-libX11-devel}
BuildRequires:	zlib-devel
%if %{with qt}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5WebEngine-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	qt5-qmake
%endif
Requires:	aspell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Recoll is a desktop search tool that provides full text search (from
single-word to arbitrarily complex boolean searches) in a GUI with few
mandatory external dependencies. It uses the Xapian information
retrieval library as its storage and retrieval engine.

%package qt
Summary:	A GUI for Recoll based on Qt 5
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
A GUI for Recoll based on Qt 5.

%prep
%setup -q

grep -rl '#!.*env python' -l filters | xargs %{__sed} -i -e '1s,#!.*env python3$,#!%{__python3},'

%build
%configure \
	QMAKE=%{_bindir}/qmake-qt5 \
	ac_cv_path_aspellProg=%{_bindir}/aspell \
	ac_cv_path_fileProg=%{_bindir}/file \
	--enable-idxthreads \
	--disable-python-chm \
	--disable-python-module \
	--enable-recollq \
	--with-fam=no \
	%{?with_qt:--enable-webengine} \
	%{!?with_qt:--disable-qtgui} \
	%{!?with_x11:--disable-x11mon}
%{__make} \
	librcldir=%{_libdir}

cd python/recoll
%py3_build
cd ../pychm
%py3_build
cd ../..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	librcldir=%{_libdir}

cd python/recoll
%py3_install
cd ../pychm
%py3_install
cd ../..

rm $RPM_BUILD_ROOT%{_datadir}/recoll/doc/{docbook-xsl.css,usermanual.html}
ln -s %{_docdir}/%{name}-%{version}/{docbook-xsl.css,usermanual.html} $RPM_BUILD_ROOT%{_datadir}/recoll/doc

%{__rm} $RPM_BUILD_ROOT%{_libdir}/librecoll.{so,la}

%{?with_qt:%find_lang %{name} --with-qm}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog README doc/user/{docbook-xsl.css,usermanual.html}
%attr(755,root,root) %{_bindir}/recollindex
%attr(755,root,root) %{_bindir}/recollq
%attr(755,root,root) %{_libdir}/librecoll-%{version}.so
%{_mandir}/man1/recollindex.1*
%{_mandir}/man1/recollq.1*
%{_mandir}/man5/recoll.conf.5*
%dir %{_datadir}/recoll
%{_datadir}/recoll/doc
%{_datadir}/recoll/examples
%dir %{_datadir}/recoll/filters
%{_datadir}/recoll/filters/abiword.xsl
%attr(755,root,root) %{_datadir}/recoll/filters/cmdtalk.py
%attr(755,root,root) %{_datadir}/recoll/filters/conftree.py
%{_datadir}/recoll/filters/fb2.xsl
%{_datadir}/recoll/filters/gnumeric.xsl
%attr(755,root,root) %{_datadir}/recoll/filters/hotrecoll.py
%attr(755,root,root) %{_datadir}/recoll/filters/kosplitter.py
%{_datadir}/recoll/filters/msodump.zip
%{_datadir}/recoll/filters/okular-note.xsl
%{_datadir}/recoll/filters/opendoc-body.xsl
%{_datadir}/recoll/filters/opendoc-flat.xsl
%{_datadir}/recoll/filters/opendoc-meta.xsl
%{_datadir}/recoll/filters/openxml-meta.xsl
%{_datadir}/recoll/filters/openxml-word-body.xsl
%{_datadir}/recoll/filters/openxml-xls-body.xsl
%attr(755,root,root) %{_datadir}/recoll/filters/ppt-dump.py
%attr(755,root,root) %{_datadir}/recoll/filters/rcl7z
%attr(755,root,root) %{_datadir}/recoll/filters/rclaptosidman
%attr(755,root,root) %{_datadir}/recoll/filters/rclaudio
%attr(755,root,root) %{_datadir}/recoll/filters/rclbasehandler.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclbibtex.sh
%attr(755,root,root) %{_datadir}/recoll/filters/rclcheckneedretry.sh
%attr(755,root,root) %{_datadir}/recoll/filters/rclchm
%attr(755,root,root) %{_datadir}/recoll/filters/rclconfig.py
%attr(755,root,root) %{_datadir}/recoll/filters/rcldia
%attr(755,root,root) %{_datadir}/recoll/filters/rcldjvu.py
%attr(755,root,root) %{_datadir}/recoll/filters/rcldoc.py
%attr(755,root,root) %{_datadir}/recoll/filters/rcldvi
%attr(755,root,root) %{_datadir}/recoll/filters/rclepub
%attr(755,root,root) %{_datadir}/recoll/filters/rclepub1
%attr(755,root,root) %{_datadir}/recoll/filters/rclexec1.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclexecm.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclfb2.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclgaim
%attr(755,root,root) %{_datadir}/recoll/filters/rclgenxslt.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclhwp.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclics
%attr(755,root,root) %{_datadir}/recoll/filters/rclimg
%attr(755,root,root) %{_datadir}/recoll/filters/rclimg.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclinfo
%attr(755,root,root) %{_datadir}/recoll/filters/rclkar
%attr(755,root,root) %{_datadir}/recoll/filters/rclkwd
%attr(755,root,root) %{_datadir}/recoll/filters/rcllatinclass.py
%{_datadir}/recoll/filters/rcllatinstops.zip
%attr(755,root,root) %{_datadir}/recoll/filters/rcllyx
%attr(755,root,root) %{_datadir}/recoll/filters/rclman
%attr(755,root,root) %{_datadir}/recoll/filters/rclmidi.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclocr.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclocrabbyy.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclocrcache.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclocrtesseract.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclopxml.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclpdf.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclppt.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclps
%attr(755,root,root) %{_datadir}/recoll/filters/rclpst.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclpurple
%attr(755,root,root) %{_datadir}/recoll/filters/rclpython.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclrar
%attr(755,root,root) %{_datadir}/recoll/filters/rclrtf.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclscribus
%attr(755,root,root) %{_datadir}/recoll/filters/rclshowinfo
%attr(755,root,root) %{_datadir}/recoll/filters/rcltar
%attr(755,root,root) %{_datadir}/recoll/filters/rcltex
%attr(755,root,root) %{_datadir}/recoll/filters/rcltext.py
%attr(755,root,root) %{_datadir}/recoll/filters/rcluncomp
%attr(755,root,root) %{_datadir}/recoll/filters/rcluncomp.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclwar
%attr(755,root,root) %{_datadir}/recoll/filters/rclxls.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclxml.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclxmp.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclxslt.py
%attr(755,root,root) %{_datadir}/recoll/filters/rclzip
%attr(755,root,root) %{_datadir}/recoll/filters/recoll-we-move-files.py
%{_datadir}/recoll/filters/recollepub.zip
%{_datadir}/recoll/filters/svg.xsl
%attr(755,root,root) %{_datadir}/recoll/filters/xls-dump.py
%attr(755,root,root) %{_datadir}/recoll/filters/xlsxmltocsv.py
%{_datadir}/recoll/filters/xml.xsl
%dir %{_datadir}/recoll/translations
%dir %{py3_sitedir}/recoll
%{py3_sitedir}/recoll/*.py
%{py3_sitedir}/recoll/__pycache__
%attr(755,root,root) %{py3_sitedir}/recoll/_recoll.cpython-*.so
%{py3_sitedir}/Recoll-*-py3*.egg-info
%dir %{py3_sitedir}/recollchm
%{py3_sitedir}/recollchm/*.py
%{py3_sitedir}/recollchm/__pycache__
%attr(755,root,root) %{py3_sitedir}/recollchm/_chmlib.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/recollchm/extra.cpython-*.so
%{py3_sitedir}/recollchm-*-py3*.egg-info


%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/recoll
%{_mandir}/man1/recoll.1*
%{_datadir}/metainfo/recoll.appdata.xml
%{_desktopdir}/recoll-searchgui.desktop
%{_iconsdir}/hicolor/*x*/apps/recoll.png
%{_pixmapsdir}/recoll.png
%{_datadir}/recoll/images
%endif
