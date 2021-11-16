# 1- Selecciones conjuntivas
      σθ1∧θ2(E) = σθ1(σθ2(E))
      <----------------------
        Derecha a izquierda
      

      { "type" : "sigma",
        "cond" : {   "type" : "eq",
                      "values" : ["edad", 18]
                  },
        "rel" : {"type" : "sigma",
                 "cond" : {   "type" : "eq",
                      "values" : ["sexo", "hombre"]
                  }
                 "rel" : "Persona"
                },
      }
        ----------------->
      { "type" : "sigma",
        "cond" : {	"type" : "and",
                        "values" : [ 
                                    {	"type" : "eq",
                                          "values" : ["edad", 18]
                                    },
                                    {	"type" : "eq",
                                          "values" : ["sexo", "hombre"]
                                    }
                              ]
                        },
        "rel" : Persona
      }
-----------

# 2-Selecciones conmutativas

      σθ1(σθ2(E)) = σθ2(σθ1(E))
      Ordenadas alfabéticamente
      
      { "type" : "sigma",
        "cond" : {	"type" : "eq",
                        "values" : ["sexo", "hombre"]
                  },
        "rel" : {"type" : "sigma",
                 "cond" :{   "type" : "eq",
                            "values" : ["edad", 18]
                        },
                 "rel" : Persona
                }
      }
      ------------------> (ordena alfabéticamente)
      { "type" : "sigma",
        "cond" : {   "type" : "eq",
                      "values" : ["edad", 18]
                  }
        "rel" : {"type" : "sigma",
                 "cond" :{	"type" : "eq",
                              "values" : ["sexo", "hombre"]
                        },
                 "rel" : Persona
                }
      }
      
---------

# 3-Cascada de proyecciones
  
      ΠL1(ΠL2(. . .(ΠLn(E)). . .)) = ΠL1(E)
  
    {   "type" : "pi",
        "proj" : nombre,
        "rel" : {   "type" : "pi",
                      "proj" : edad,
                      "rel" : {   "type" : "pi",
                                    "proj" : sexo,
                                    "rel" : Persona
                               }
                  }
    }
    ----------------------------------------------->
    {   "type" : "pi",
        "proj" : nombre,
        "rel" : Persona
    }
    
-------

# 4-  El select de un producto cartesiano, es igual que un natural join
       a.
       σθ(E1 × E2) = E1 ⊲⊳θ E2
      -----------------------> Lo dejamos como natural join

    {   "type" : "sigma",
        "cond" : {	"type" : "eq",
                        "values" : ["nombre", "Juan"]
                  },
        "rel" : {"type" : "pro",
                    "lrel" : tabla1,
                    "rrel" : tabla2
                }
     }
     ------------------------------>
     {  "type" : "join",
        "cond" : {	"type" : "eq",
                        "values" : ["nombre", "Juan"]
                  },
        "lrel" : tabla1,
        "rrel" : tabla2
    }
    
       b. La selección de un theta join, es este theta join con dos condiciones
      σθ1(E1 ⊲⊳σθ2E2) = E1 ⊲⊳θ1∧θ2 E2 
   
    {   "type" : "sigma",
        "cond" : {   "type" : "eq",
                      "values" : ["edad", 18]
                  },
        "rel" : {  "type" : "join",
                    "cond" :{	"type" : "eq",
                              "values" : ["nombre", "Juan"]
                             },
                    "lrel" : tabla1,
                    "rrel" : tabla2
                 }
    }
    --------------------------------------->
    {  "type" : "join",
        "cond" : {	"type" : "and",
                        "values" : [ 
                                    {	"type" : "eq",
                                          "values" : ["edad", 18]
                                    },
                                    {	"type" : "eq",
                                          "values" : ["nombre", "Juan"]
                                    }
                              ]
                        },
        "lrel" : tabla1,
        "rrel" : tabla2
    }
    
--------

# 5-Los theta join son conmutativos
      E1 ⊲⊳θ E2 = E2 ⊲⊳θ E1
      Ordenados alfabéticamente
  
    {  "type" : "join",
        "cond" : {	"type" : "eq",
                        "values" : ["nombre", "Juan"]
                  },
        "lrel" : Personas,
        "rrel" : Jugadores
    }
    --------------------------->
    {  "type" : "join",
        "cond" : {	"type" : "eq",
                        "values" : ["nombre", "Juan"]
                  },
        "lrel" : Jugadores,
        "rrel" : Personas
    }

--------

# 6-Los natural join/theta join son asociativos
    (E1 ⊲⊳ E2) ⊲⊳ E3 = E1 ⊲⊳ (E2 ⊲⊳ E3)
    El objeto "lrel" del JSON es simple, y en la derecha en la que sea el objeto. De esta manera queda más ordenado
    Natural join
    
    {  "type" : "pro",,
        "lrel" : {  "type" : "pro",
                      "lrel" : Personas,
                      "rrel" : Jugadores
                  },
        "rrel" : Ganadores
    }
    ---------------------------------------->
    {  "type" : "pro"
        "lrel" : Personas,
        "rrel" : {  "type" : "pro"
                      "lrel" : Jugadores,
                      "rrel" : Ganadores
                  }
    }
    
    (E1 ⊲⊳θ1 E2) ⊲⊳θ2∧θ3 E3 = E1 ⊲⊳θ1∧θ3(E2 ⊲⊳θ2 E3)
    Theta join
    Theta1: nombre = Juan
    Theta2: edad = 18
    Theta3: sexo = hombre
    
    {  "type" : "join",
        "cond" : {   "type" : "eq",
                      "values" : ["nombre", "Juan"]
                  }
        "lrel" : {  "type" : "join",
                      "cond" : {	"type" : "and",
                                    "values" : [ 
                                                {	"type" : "eq",
                                                      "values" : ["edad", 18]
                                                },
                                                {	"type" : "eq",
                                                      "values" : ["sexo", "hombre"]
                                                }
                                          ]
                                    },
                      "lrel" : Personas,
                      "rrel" : Jugadores
                  },
        "rrel" : Ganadores
    }
    ---------------------------------------->
    {  "type" : "join",
        "cond" : {	"type" : "and",
                        "values" : [ 
                                    {	"type" : "eq",
                                          "values" : ["nombre", "Juan"]
                                    },
                                    {	"type" : "eq",
                                          "values" : ["sexo", "hombre"]
                                    }
                              ]
                        },
        "lrel" : Personas,
        "rrel" : {  "type" : "join",
                      "cond" : {   "type" : "eq",
                                  "values" : ["edad", 18]
                              },
                      "lrel" : Jugadores,
                      "rrel" : Ganadores
                  }
    }
    
--------

# 7-Selects de theta joins
    
      TABLAS:
      PERSONAS ------NOMBRE----EDAD----SEXO
      GANADORES -----NOMBRE----PREMIO
      
      La condición theta0 es de un atributo que solo está en la tabla 1 (PERSONAS)
      Theta: nombre=Juan
      Theta0: edad=18
      
      A.
      σθ0(E1 ⊲⊳θ E2) = (σθ0(E1)) ⊲⊳θ E2
      <--------------------------------- Dejamos el select primero
      
       {  "type" : "join",
          "cond" : {   "type" : "eq",
                      "values" : ["nombre", "Juan"]
                  },
          "lrel" : {  "type" : "sigma",
                      "cond" : {   "type" : "eq",
                                   "values" : ["edad", 18]
                               },
                      "rel" : Personas
                    },
          "rrel" : Ganadores
      }
      ------------------------------->
      {   "type" : "sigma",
          "cond" : {   "type" : "eq",
                       "values" : ["edad", 18]
                   },
          "rel" : {   "type" : "join",
                      "cond" : {   "type" : "eq",
                                   "values" : ["nombre", "Juan"]
                               },
                      "lrel" : Personas,
                      "rrel" : Ganadores
                  }
      }
      
      B.  
      σθ1∧θ2(E1 ⊲⊳θ E2) = (σθ1(E1)) ⊲⊳θ (σθ2(E2))
      <------------------------------------- Dejamos el select primero
      
      Theta1 es de un atributo que solo está en E1(Personas) y Theta2 es de un atributo que solo está en E2(Ganadores)
      Theta: nombre=Juan
      Theta1: edad=18
      Theta2: premio=Mundial
      
      {   "type" : "join",
          "cond" : {   "type" : "eq",
                      "values" : ["nombre", "Juan"]
                  },
          "lrel" : {  "type" : "sigma",
                      "cond" : {   "type" : "eq",
                                   "values" : ["edad", 18]
                               },
                      "rel" : Personas
                    },
          "rrel" : {  "type" : "sigma",
                      "cond" : {   "type" : "eq",
                                   "values" : ["premio", "Mundial"]
                               }
                      "rel" : Ganadores
                    }
      }
      --------------------------------------->
       {   "type" : "sigma",
          "cond" : {	"type" : "and",
                        "values" : [ 
                                    {	"type" : "eq",
                                          "values" : ["edad", 18]
                                    },
                                    {	"type" : "eq",
                                          "values" : ["premio", "Mundial"]
                                    }
                              ]
                        },
          "rel" : {   "type" : "join",
                      "cond" : {   "type" : "eq",
                            "values" : ["nombre", "Juan"]
                        },
                      "lrel" : Personas,
                      "rrel" : Ganadores
                  }
      }

----------

# 8-La proyección se distribuye en theta join

      TABLAS:
      PERSONAS ------NOMBRE----EDAD----SEXO
      GANADORES -----NOMBRE----PREMIO----NACIONALIDAD
  
      A.
      ΠL1∪L2(E1 ⊲⊳θ E2) = (ΠL1(E1)) ⊲⊳θ (ΠL2(E2))
      <---------------------------------------- Dejamos la proyección al principio
      
      L1 es un atributo que solo está en E1(Personas) y L2 de E2(Ganadores)
      Theta: nombre=Juan
      L1: edad
      L2: premio
  
    {   "type" : "join",
        "cond" : {   "type" : "eq",
                      "values" : ["nombre", "Juan"]
                  },
        "lrel" :  {   "type" : "pi",
                      "proj" : ["edad"],
                      "rel" : Personas
                  },
        "rrel" : {    "type" : "pi",
                      "proj" : ["premio"],
                      "rel" : ganadores
                  }
    }
     ----------------------------------->
     {  "type" : "pi",
        "proj" : [edad, premio],
        "rel" : {   "type" : "join",
                    "cond" :{   "type" : "eq",
                                  "values" : ["nombre", "Juan"]
                              },
                    "lrel" : Personas,
                    "rrel" : Ganadores
                }
    }
    
    B.
    ΠL1∪L2(E1 ⊲⊳θ E2) = ΠL1∪L2((ΠL1∪L3(E1)) ⊲⊳θ (ΠL2∪L4(E2)))
    <----------------------------------------------------------
    
    L1 es un atributo de E1(Personas) y L2 es un atributo de E2(Ganadores)
    L3 es un atributo de E1(Personas) y L4 es un atributo de E2(Ganadores)
    
    L1 es distinto de L3 y L2 es distinto de L4
    Con esta regla se pueden obviar L3 y L4 (ya que es una proyección)
    
    L1:EDAD----------Personas
    L2:PREMIO--------Ganadores
    L3:SEXO----------Personas
    L4:NACIONALIDAD--Ganadores
    Theta: nombre=Juan
    
    {   "type" : "pi",
        "proj" : [edad, premio],
        "rel" : { "type" : "join",
                  "cond" : {   "type" : "eq",
                                  "values" : ["nombre", "Juan"]
                              },
                  "lrel" :  {   "type" : "pi",
                                "proj" : [edad, sexo],
                                "rel" : Personas
                            },
                  "rrel" : {   "type" : "pi",
                                "proj" : [premio, nacionalidad],
                                "rel" : Ganadores
                            }
                }
    }
    ------------------------------------------->
    {   "type" : "pi",
        "proj" : [edad, premio],
        "rel" :{    "type" : "join",
                    "cond" :{   "type" : "eq",
                                  "values" : ["nombre", "Juan"]
                              },
                    "lrel" : Personas,
                    "rrel" : Ganadores
                }
     }


