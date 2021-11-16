
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
----------


> SELECT Nombre, Ap1, Ap2
> FROM Empl, Dedicacion
> WHERE Dni=DniEmpl 



PI[Nombre, Ap1, Ap2] (SIGMA[Dni=DniEmpl] (Empl X Dedicacion))


	{	"type"	:	"pi",
		"proj"	:	["Nombre", "Ap1", "Ap2"],
		"rel"	:	{	"type"	:	"sigma",
					"cond"	:	{	
								"type"		: 	"eq",	
								"values"	:	["Dni", "DniEmpl"]	
							}
					"rel"	:	{	
								"type"	:	"pro",
								"lrel"	:	{	"type"	:	"rel",
											"table"	:	"Empl"
										}
								"rrel"	:	{	"type"	:	"rel",
											"table"	:	"Dedicacion"
										}
							}
				}
	}
 

----------
----------


> SELECT p.nombre
> FROM curso AS c, profesor AS p
> WHERE p.nombre = "Juan Carlos" AND c.id = "IS345"



PI[p.nombre] (SIGMA[p.nombre = "Juan Carlos" AND c.id = "IS345"] (RHO[c] (curso) X RHO[p] (profesor)))


	{	"type"	:	"pi",
		"proj"	:	["Nombre", "Ap1", "Ap2"],
		"rel"	:	{	"type"	:	"sigma",
					"cond"	:	{	
								"type"		: 	"and",	
								"values"	:	[	{	"type"	:	"eq",
													"values"	: ["p.nombre", "Juan Carlos"]
												},
												{	"type"	:	"eq",
													"values"	: ["c.id", "IS345"]
												}
											]	
							}
					"rel"	:	{	
								"type"	:	"pro",
								"lrel"	:	{	"type"	:	"rho",
											"ren"	:	["curso", "c"]
											"rel"	:	{	"type"	: "rel",
														"table"	:	"curso"
													}
										}
								"rrel"	:	{	"type"	:	"rho",
											"ren"	:	["profesor", "p"]
											"rel"	:	{	"type"	: "rel",
														"table"	:	"profesor"
													}
										}
							}
				}
	}
 

----------

