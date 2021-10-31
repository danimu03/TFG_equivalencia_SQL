
----------


> SELECT Nombre
> FROM Persona
> WHERE Pais = "España"


PI[Nombre] (SIGMA[Pais="España"] (Persona))


	{	"type"	:	"pi",
		"proj"	:	["Nombre"],
		"rel"	:	{	"type"	:	"sigma",
					"cond"	:	{	
								"type"		: 	"eq",	
								"values"	:	["Pais", "España"]	
							}
					"rel"	:	{	
								"type"	:	"rel",
								"table"	:	"Persona"
							}	
				}
	}
 

----------
----------


> SELECT Nombre, Ap1, Ap2
> FROM Empl
>
> WHERE Pais = "España"


PI[Nombre] (SIGMA[Pais="España"] (Persona))


	{	"type"	:	"pi",
		"proj"	:	["Nombre"],
		"rel"	:	{	"type"	:	"sigma",
					"cond"	:	{	
								"type"		: 	"eq",	
								"values"	:	["Pais", "España"]	
							}
					"rel"	:	{	
								"type"	:	"rel",
								"table"	:	"Persona"
							}	
				}
	}
 

----------
