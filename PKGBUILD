# Maintainer: Dylan <your-email-optional>
pkgname=project-dylan-git
pkgver=1.0.0
pkgrel=1
pkgdesc="Asynchronous Minecraft DNS Subdomain and SRV Port Scanner"
arch=('any')
url="https://github.com/JDM517/PROJECT-DYLAN/tree/main"
license=('GPL3')
depends=('python' 'python-dnspython')
makedepends=('git')
provides=('project-dylan')
conflicts=('project-dylan')
source=("git+${url}.git")
sha256sums=('SKIP')

package() {
    cd "${srcdir}/${pkgname%-git}"

    # 1. Create the system directories
    install -d "${pkgdir}/usr/share/project-dylan"
    install -d "${pkgdir}/usr/bin"

    # 2. Install the primary Python source code execution bundle
    install -m 644 project_dylan.py "${pkgdir}/usr/share/project-dylan/project_dylan.py"

    # 3. Deploy the executable binary symlink command map wrapper
    install -m 755 project-dylan "${pkgdir}/usr/bin/project-dylan"
}
