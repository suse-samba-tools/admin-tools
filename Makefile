setup:
	if [ ! -e build ] ; then osc co home:dmulder:YaST:AppImage admin-tools -o build; fi
	cp admin-tools.appdata.xml build/
	cp src/clients/admin-tools.py build/
	cp appimage.yml build/

build: setup
	pushd build; osc build AppImage x86_64 appimage.yml --noverify; popd
	cp /var/tmp/build-root/AppImage-x86_64/usr/src/packages/OTHER/admin-tools-*-x86_64.AppImage admin-tools-x86_64.AppImage

rebuild: admin-tools-x86_64.AppImage
	rm -rf squashfs-root/ >/dev/null 2>&1 || echo
	./admin-tools-x86_64.AppImage --appimage-extract >/dev/null 2>&1
	rm squashfs-root/usr/share/metainfo/admin-tools.appdata.xml || echo
	cp src/clients/admin-tools.py squashfs-root/usr/share/YaST2/clients/
	appimagetool squashfs-root/
	rm -rf squashfs-root/
