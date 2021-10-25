1- Selecciones conjuntivas
      σθ1∧θ2(E) = σθ1(σθ2(E))
      <----------------------
        Derecha a izquierda
      

      { "type" : "sigma",
        "cond" : edad = 18,
        "rel" : {"type" : "sigma",
                 "cond" : sexo = hombre,
                 "rel" : Persona
                }
      }
        ----------------->
      { "type" : "sigma",
        "cond" : [edad = 18, sexo = hombre],
        "rel" : Persona
      }
     
2-Selecciones conmutativas
      σθ1(σθ2(E)) = σθ2(σθ1(E))
      Ordenadas alfabéticamente
      
      { "type" : "sigma",
        "cond" : sexo = hombre,
        "rel" : {"type" : "sigma",
                 "cond" : edad = 18,
                 "rel" : Persona
                }
      }
      ------------------> (ordena alfabéticamente)
      { "type" : "sigma",
        "cond" : edad = 18,
        "rel" : {"type" : "sigma",
                 "cond" : sexo = hombre,
                 "rel" : Persona
                }
      }
      
3-Cascada de proyecciones
  
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
    
4-  El select de un producto cartesiano, es igual que un natural join
   a.
  σθ(E1 × E2) = E1 ⊲⊳θ E2
  -----------------------> Lo dejamos como natural join

    {   "type" : "sigma",
        "cond" : nombre = Juan,
        "rel" : {"type" : "pro",
                    "lrel" : tabla1,
                    "rrel" : tabla2
                }
     }
     ------------------------------>
     {  "type" : "join",
        "cond" : nombre = Juan,
        "lrel" : tabla1,
        "rrel" : tabla2
    }
    
    b. La selección de un natural join, es este natural join con dos condiciones
   σθ1(E1 ⊲⊳σθ2E2) = E1 ⊲⊳θ1∧θ2 E2 
   
    {   "type" : "sigma",
        "cond" : edad=18,
        "rel" : {  "type" : "join",
                    "cond" : nombre = Juan,
                    "lrel" : tabla1,
                    "rrel" : tabla2
                 }
    }
    --------------------------------------->
    {  "type" : "join",
        "cond" : [edad = 18, nombre = Juan],
        "lrel" : tabla1,
        "rrel" : tabla2
    }
    
    
5-Los natural join son conmutativos
  E1 ⊲⊳θ E2 = E2 ⊲⊳θ E1
  Ordenados alfabéticamente
  
    {  "type" : "join",
        "cond" : nombre = Juan,
        "lrel" : Personas,
        "rrel" : Jugadores
    }
    --------------------------->
    {  "type" : "join",
        "cond" : nombre = Juan,
        "lrel" : Jugadores,
        "rrel" : Personas
    }
    
6-Los natural join son asociativos
    (E1 ⊲⊳ E2) ⊲⊳ E3 = E1 ⊲⊳ (E2 ⊲⊳ E3)
    El objeto "lrel" del JSON es simple, y en la derecha en la que sea el objeto. De esta manera queda más ordenado
    
    {  "type" : "join",
        "cond" : ---------,
        "lrel" : {  "type" : "join",
                      "cond" : ---------,
                      "lrel" : Personas,
                      "rrel" : Jugadores
                  },
        "rrel" : Ganadores
    }
    ---------------------------------------->
    {  "type" : "join",
        "cond" : ---------,
        "lrel" : Personas,
        "rrel" : {  "type" : "join",
                      "cond" : ---------,
                      "lrel" : Jugadores,
                      "rrel" : Ganadores
                  }
    }
    
    
    
    (E1 ⊲⊳θ1 E2) ⊲⊳θ2∧θ3 E3 = E1 ⊲⊳θ1∧θ3(E2 ⊲⊳θ2 E3)
    
    {  "type" : "join",
        "cond" : nombre=Juan,
        "lrel" : {  "type" : "join",
                      "cond" : [edad=18, sexo=hombre],
                      "lrel" : Personas,
                      "rrel" : Jugadores
                  },
        "rrel" : Ganadores
    }
    ---------------------------------------->
    {  "type" : "join",
        "cond" : [nombre = Juan, sexo=hombre],
        "lrel" : Personas,
        "rrel" : {  "type" : "join",
                      "cond" : edad = 18,
                      "lrel" : Jugadores,
                      "rrel" : Ganadores
                  }
    }
    
    
    7-Selects de natural joins
    
      TABLAS:
      PERSONAS ------NOMBRE----EDAD----SEXO
      GANADORES -----NOMBRE----PREMIO
      
      A.
      σθ0(E1 ⊲⊳θ E2) = (σθ0(E1)) ⊲⊳θ E2
      <--------------------------------- Dejamos el select primero
      
       {  "type" : "join",
          "cond" : ------------------,
          "lrel" : {  "type" : "sigma",
                      "cond" : edad = 18,
                      "rel" : Personas
                    },
          "rrel" : Ganadores
      }
      ------------------------------->
      {   "type" : "sigma",
          "cond" : edad = 18,
          "rel" : {   "type" : "join",
                      "cond" : --------------,
                      "lrel" : Personas,
                      "rrel" : Ganadores
                  }
      }
      
      B.  
      σθ1∧θ2(E1 ⊲⊳θ E2) = (σθ1(E1)) ⊲⊳θ (σθ2(E2))
      <------------------------------------- Dejamos el select primero
      
      
      {   "type" : "join",
          "cond" : ------------------,
          "lrel" : {  "type" : "sigma",
                      "cond" : edad = 18,
                      "rel" : Personas
                    },
          "rrel" : {  "type" : "sigma",
                      "cond" : premio = Mundial,
                      "rel" : Ganadores
                    }
      }
      --------------------------------------->
       {   "type" : "sigma",
          "cond" : [edad = 18, premio = Mundial],
          "rel" : {   "type" : "join",
                      "cond" : --------------,
                      "lrel" : Personas,
                      "rrel" : Ganadores
                  }
      }

8-La proyección se distribuye en theta join

  TABLAS:
  PERSONAS ------NOMBRE----EDAD----SEXO
  GANADORES -----NOMBRE----PREMIO----NACIONALIDAD
  
  A.
  ΠL1∪L2(E1 ⊲⊳θ E2) = (ΠL1(E1)) ⊲⊳θ (ΠL2(E2))
  <---------------------------------------- Dejamos la proyección al principio
  
    {   "type" : "join",
        "cond" : --------------,
        "lrel" :  {   "type" : "pi",
                      "proj" : edad,
                      "rel" : Personas
                  },
        "rrel" : {    "type" : "pi",
                      "proj" : premio,
                      "rel" : ganadores
                  }
    }
     ----------------------------------->
     {  "type" : "pi",
        "proj" : [edad, premio],
        "rel" : {   "type" : "join",
                    "cond" : ----------,
                    "lrel" : Personas,
                    "rrel" : Ganadores
                }
    }
    
    B.
    ΠL1∪L2(E1 ⊲⊳θ E2) = ΠL1∪L2((ΠL1∪L3(E1)) ⊲⊳θ (ΠL2∪L4(E2)))
    <----------------------------------------------------------
    
    L1:EDAD----------Personas
    L2:PREMIO--------Ganadores
    L3:SEXO----------Personas
    L4:NACIONALIDAD--Ganadores
    
    {   "type" : "pi",
        "proj" : [edad, premio],
        "rel" : { "type" : "join",
                  "cond" : -----------,
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
                    "cond" : -----------,
                    "lrel" : Personas,
                    "rrel" : Ganadores
                }
     }


