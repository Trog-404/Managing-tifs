CC=gcc
CFLAGS=-fPIC -shared
LIBNAME=libmetadata_add.so

$(LIBNAME): metadata_add.c
	$(CC) $(CFLAGS) metadata_add_module.c -o $(LIBNAME) -ltiff

clean:
	rm -f $(LIBNAME)
