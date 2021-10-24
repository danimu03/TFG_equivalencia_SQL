# Projection

    {   "type" : "pi",
        "proj" : |projection| / [|projections|],
        "rel" : |relation| / {|other operation|}
    }


----------


# Selection

    {   "type" : "sigma",
        "cond" : [|conditions|],
        "rel" : |relation| / {|other operation|}
    }
    
_*Falta definir el formato de las condiciones_

----------


# Rename

    {   "type" : "rho",
        "ren" : ["|name|" , "|rename|"],
        "rel" : |relation| / {|other operation|}
    }

----------

# Cartesian product

    {   "type" : "pro",
        "lrel" : |relation| / {|other operation|},
        "rrel" : |relation| / {|other operation|}
    }


----------

# Natural join 

    {   "type" : "join",
        "cond" : [|conditions|],
        "lrel" : |relation| / {|other operation|},
        "rrel" : |relation| / {|other operation|}
    }
    
_*Falta definir el formato de las condiciones_


----------