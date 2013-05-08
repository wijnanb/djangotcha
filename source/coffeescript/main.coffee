# FIX console for IE<9
if typeof console is "undefined"
    window.console =
        log: ->
        warn: ->
        error: ->