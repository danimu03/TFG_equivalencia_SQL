

----------
<p>* Los elementos entre barras tienen sus propias definiciones</p>

----------



# Projection

    {   "type" : "pi",
        "proj" : [projections],
        "rel" : {|relation|} / {|other operation|}
    }


----------


# Selection

    {   "type" : "sigma",
        "cond" : {|conditions|},
        "rel" : {|relation|} / {|other operation|}
    }
    

----------


# Rename

    {   "type" : "rho",
        "ren" : ["name" , "rename"],
        "rel" : {|relation|} / {|other operation|}
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
        "cond" : {|conditions|},
        "lrel" : {|relation|} / {|other operation|},
        "rrel" : {|relation|} / {|other operation|}
    }
    


----------


# Relation

	{   "type" : "rel",
	    "table" : "name"
	}


----------


# Conditions

###Examples

simple condition -> dni = "0230098R"

	{   "type" : "eq",
	    "values" : ["dni", "0230098R"]
	}

double condition -> id = 00012 AND dni = "0230098R"
	
	{	"type" : "and",
		"values" : [ 
				{	"type" : "eq",
       					"values" : ["id", 00012]
				},
        			{	"type" : "eq",
        				"values" : ["dni", "0230098R"]
				}
			]
    	}


various conditions -> id = 00012 AND ( puesto = "técnico" OR puesto = "ayudante")

	{   "type" : "and",
	    "values" : [ 
			       {	"type" : "eq",
       					"values" : ["id", 00012]
			       },
        		       {	"type" : "or",
        				"values" : [
							{	"type" : "eq",
								"values" : ["puesto", "técnico"]
							},
					        	{	"type" : "eq",
					        		"values" : ["puesto", "técnico"]
							}
						   ]
				}
			]
    }

----------
