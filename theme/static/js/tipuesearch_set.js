/*
Tipue Search 7.1
Copyright (c) 2019 Tipue
Tipue Search is released under the MIT License
http://www.tipue.com/search
*/

/*
Stop words
Stop words list from http://www.ranks.nl/stopwords
*/

var tipuesearch_stop_words = []

// Word replace

var tipuesearch_replace = { words: [] }

// Weighting

var tipuesearch_weight = { weight: [] }

var tipuesearch_related = {
    Related: [
        {
            search: 'testwort',
            related: 'raspberry pi',
        },
    ],
}

// Stemming
var tipuesearch_stem = { words: [] }

// Internal strings

var tipuesearch_string_1 = 'Pas de titre'
var tipuesearch_string_2 = 'Résultats pour'
var tipuesearch_string_3 = 'Search instead for'
var tipuesearch_string_4 = '1 résultats'
var tipuesearch_string_5 = 'resultats'
var tipuesearch_string_6 = 'Précédent'
var tipuesearch_string_7 = 'Suivant'
var tipuesearch_string_8 = 'Aucun résultat'
var tipuesearch_string_9 = 'Les mots trop communs sont ignorés'
var tipuesearch_string_10 = 'Recherche trop courte'
var tipuesearch_string_11 = "Doit être d'au moins un caractère"
var tipuesearch_string_12 = "Doit être d'au moins"
var tipuesearch_string_13 = 'caractères'
var tipuesearch_string_14 = '&lt;&lt;'
var tipuesearch_string_15 = '&gt;&gt;'
var tipuesearch_string_16 = 'page(s) of results.'
var tipuesearch_string_17 = 'Score:'
var tipuesearch_string_18 = 'Search took $1 seconds.'
