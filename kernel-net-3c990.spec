#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
%define		_orig_name	3c990

Summary:	Linux driver for the 3Com 3C990 Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych 3Com 3C990
Name:		kernel-net-%{_orig_name}
Version:	1.0.0a
%define	_rel	10
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://support.3com.com/infodeli/tools/nic/linux/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	e7597b2747a18f0cfe7bc81e83a2bc68
Patch0:		%{_orig_name}-redefine.patch
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This driver (3c990.c) has been written to work with the 3c990 product
line of network cards, manufactured by 3Com Corp.

This driver is not intended for any other product line, including the
3c59x or 3c90x product lines (although drivers with both of these
names, and for both of these product lines, are available). 

%description -l pl
Sterownik dla Linuksa do kart sieciowych 3Com 3c990.

Nie obs³uguje kart serii 3c59x i 3c90x, istniej± inne sterowniki do
tych linii produktów.

%package -n kernel-smp-net-%{_orig_name}
Summary:        Linux SMP driver for the 3Com 3C990 Network Interface Cards
Summary(pl):    Sterownik dla Linuksa SMP dla kart sieciowych 3Com 3C990
Release:        %{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-%{_orig_name}
This driver (3c990.c) has been written to work with the 3c990 product
line of network cards, manufactured by 3Com Corp on SMP systems.

This driver is not intended for any other product line, including the
3c59x or 3c90x product lines (although drivers with both of these
names, and for both of these product lines, are available).

%description -n kernel-smp-net-%{_orig_name} -l pl
Sterownik dla Linuksa SMP do kart sieciowych 3Com 3c990.

Nie obs³uguje kart serii 3c59x i 3c90x, istniej± inne sterowniki do
tych linii produktów.

%prep
%setup -q -n %{_orig_name}-%{version} -c
%patch0 -p0

%build
rm -f %{_orig_name}.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -DSMP=1 -D__SMP__ -DCONFIG_X86_LOCAL_APIC -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c
mv -f %{_orig_name}.o %{_orig_name}-smp.o
%{kgcc} -o %{_orig_name}.o -c %{rpmcflags}  -c -DMODULE -D__KERNEL__ -O2 -Wall -Wstrict-prototypes -I%{_kernelsrcdir}/include %{_orig_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc README 
/lib/modules/%{_kernel_ver}smp/misc/*
