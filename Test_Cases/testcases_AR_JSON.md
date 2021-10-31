
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
> JOIN Proyecto ON Dni = DniDir



PI[Nombre, Ap1, Ap2] ((Empl) JOIN [Dni = DniDir] (Proyeccto))


	{	"type"	:	"pi",
		"proj"	:	["Nombre", "Ap1", "Ap2"],
		"rel"	:	{	"type"	:	"join",
					"cond"	:	{	
								"type"		: 	"eq",	
								"values"	:	["Dni", "DniDir"]	
							}
					"lrel"	:	{	
								"type"	:	"rel",
								"table"	:	"Empl"
							}
					"rrel"	:	{	
								"type"	:	"rel",
								"table"	:	"Proyecto"
							}
				}
	}
 

----------
