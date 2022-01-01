all: style.css vorheader.css basis.css normalize.css symbole.css fonts.css entwicklung.css #formular.css

#formular.css: ../scss/_formular.scss
#	sassc ../scss/_formular.scss formular.css

style.css: ../scss/style.scss
	sassc ../scss/style.scss style.css

%.css: ../scss/_%.scss
	sassc ../scss/$< $@

