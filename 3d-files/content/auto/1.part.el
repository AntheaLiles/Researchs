;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "1.part"
 (lambda ()
   (TeX-add-symbols
    '("extensiblecolor" 1)
    '("domainecolor" 1)
    '("flatcolor" 1)
    '("fosscolor" 1))
   (LaTeX-add-labels
    "fig:enter-label"
    "fig:mon_graphique"))
 :latex)

