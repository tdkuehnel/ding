# make wird benutzt, um die scss Dateien im static/scss Verzeichnis zu compilieren

CODE_DIR = static

.PHONY: project_css

project_css:
	$(MAKE) -C $(CODE_DIR)
