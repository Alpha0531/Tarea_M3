import mesa

import random

import math

class Build(mesa.Agent):

    def __init__(self, unique_id, model, color):

        super().__init__(unique_id, model)

        self.contador = 0

        self.color = color

    def step(self):

        self.contador += 1

class Tope(mesa.Agent):

    def __init__(self, unique_id, model):
        
        super().__init__(unique_id, model)
        
        self.color = "brown"
        
        self.arribados = 0
    
    def eliminar(self): 
        
        contenido = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(contenido) > 1:
        
            for i in contenido:
        
                if type(i) == Coche:
        
                    i.finalizado = True
        
                    self.model.grid.remove_agent(i)
        
                    self.arribados += 1

    def step(self):
        
        self.eliminar()

class Detenedor(mesa.Agent):
    
    def __init__(self,unique_id,model, comparacion, color):
        
        super().__init__(unique_id, model)
        
        self.cocheDetenido = []
        
        self.Detenedor2 = []
        
        self.direccionComparacion = comparacion
        
        self.color = color

    def semaforoLibre(self):
        
        posicion = []
        
        posicion.append(self.pos)
        
        if self.direccionComparacion == "Arriba":
        
            temp = list(posicion[0])
        
            temp[1] += 1
        
            posicion = tuple(temp)
        
        else:
        
            temp = list(posicion[0])
        
            temp[0] += 1
        
            posicion = tuple(temp)

        contenido = self.model.grid.get_cell_list_contents(posicion)

        if len(contenido) == 1:
        
            return True
        
        else:
        
            return False
    
    def dejarPasar(self):

        if len(self.cocheDetenido) > 0:
        
            self.cocheDetenido[0].avanza = True
        
            self.cocheDetenido.clear()
        
        else: 
        
            pass

    def step(self):
        
        if self.semaforoLibre() or self.Detenedor2[0].semaforoLibre():
        
            self.dejarPasar()
        
            self.Detenedor2[0].dejarPasar()
        
        else:
        
            contenido = self.model.grid.get_cell_list_contents(self.pos)
        
            if len(contenido) > 1:
        
                for i in contenido:
        
                    if type(i) == Coche:
        
                        self.cocheDetenido.append(i)
        
                        i.avanza = False

class TrafficLigth(mesa.Agent):

    def __init__(self, unique_id, model, pos):
        
        super().__init__(unique_id, model)
        
        self.color = "yellow"
        
        self.prioridad = []
        
        self.contadorColor = 0
        
        self.agenteSemaforoSecundario = None
        
        self.activo = True

        self.posOriginal = pos

        self.pos_X = self.posOriginal[0]

        self.pos_Y = self.posOriginal[1]
        
        self.tiempoActualOrigen = 0

        self.tiempoReactivacion = 0

    def cambioColor(self): 
       
        if self.contadorColor == 1:
       
            self.color = "red"
       
        elif self.contadorColor == 2:
       
            self.color = "green"
       
        else:
       
            self.color = "yellow"
       
            self.contadorColor = 0

    def asignacion(self):
        
        contenidoMismaCelda = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(contenidoMismaCelda) > 1:
        
            for i in contenidoMismaCelda:
        
                if type(i) == Coche:
        
                    i.avanza = False 
        
                    i.arribado = True
        
                    self.prioridad.append(i)
        
                    self.contadorColor = 1

    def vaciado(self): 
        
        if len(self.prioridad) > 0:
        
            self.prioridad.clear()
        
            self.cambioColor()

    def sinCochesCruzando(self):

        contenidosDerecha = self.model.grid.get_cell_list_contents(tuple([self.pos_X + 1 , self.pos_Y]))
        
        contenidosArriba = self.model.grid.get_cell_list_contents(tuple([self.pos_X , self.pos_Y + 1]))
        

        if len(contenidosDerecha) == 0 or len(contenidosArriba) == 0:

            self.contadorColor = 2 
            
            self.cambioColor()

            return True
        
        else:

            self.contadorColor = 1
            
            self.cambioColor()
           
            return False

    def negociacion(self):    

        vecinos = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        for i in vecinos: 
        
            contenido = self.model.grid.get_cell_list_contents(i) 
            
            if len(contenido) > 1:
            
                for j in contenido:
            
                    if type(j) == TrafficLigth:
            
                        self.agenteSemaforoSecundario = j
        
        semaforoSecundario = self.agenteSemaforoSecundario
        

        if self.contadorColor == 1:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 2
            
                semaforoSecundario.cambioColor()

        if self.contadorColor == 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 1
            
                semaforoSecundario.cambioColor()

        if self.contadorColor != 1 and self.contadorColor != 2:
            
            self.cambioColor()
            
            semaforoSecundario.contadorColor = 4
            
            semaforoSecundario.cambioColor() 
            
        try:
            
            if len(semaforoSecundario.prioridad) == 0:

                if self.sinCochesCruzando():
            
                    self.contadorColor = 2
            
                    semaforoSecundario.contadorColor = 1

                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                    if self.contadorColor == 1:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 2

                        semaforoSecundario.cambioColor()

                    if self.contadorColor == 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 1

                        semaforoSecundario.cambioColor()
                            
                    if self.contadorColor != 1 and self.contadorColor != 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 4

                        semaforoSecundario.cambioColor() 
                        

                else:

                    self.contadorColor = 2

                    semaforoSecundario.contadorColor = 1


                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                    if self.contadorColor == 1:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 2

                        semaforoSecundario.cambioColor()

                    if self.contadorColor == 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 1

                        semaforoSecundario.cambioColor()
                            
                    if self.contadorColor != 1 and self.contadorColor != 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 4

                        semaforoSecundario.cambioColor() 

            elif len(semaforoSecundario.prioridad) > 0:
                if semaforoSecundario.prioridad[0].velocidad > self.prioridad[0].velocidad: 

                    semaforoSecundario.contadorColor = 2

                    self.contadorColor = 1

                    self.cambioColor()
                    semaforoSecundario.cambioColor()

                    semaforoSecundario.prioridad[0].avanza = True


                elif semaforoSecundario.prioridad[0].velocidad < self.prioridad[0].velocidad:

                    semaforoSecundario.contadorColor = 1

                    self.contadorColor = 2

                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                else:

                    paso = random.randint(0,1)

                    if paso == 0:

                        semaforoSecundario.contadorColor = 2

                        self.contadorColor = 1

                        self.cambioColor()

                        semaforoSecundario.cambioColor()

                        semaforoSecundario.prioridad[0].avanza = True

                    else:

                        semaforoSecundario.contadorColor = 1

                        self.contadorColor = 2
                        
                        self.cambioColor()
                        
                        semaforoSecundario.cambioColor()
                        
                        self.prioridad[0].avanza = True
                        
                        self.vaciado()

        except: 

            if self.contadorColor == 1:
            
                        self.cambioColor()
            
                        semaforoSecundario.contadorColor = 2
            
                        semaforoSecundario.cambioColor()

            if self.contadorColor == 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 1
            
                semaforoSecundario.cambioColor()
                            
            if self.contadorColor != 1 and self.contadorColor != 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 4
            
                semaforoSecundario.cambioColor()      
                   
            pass
    
    def step(self): 

        if len(self.prioridad) == 0:
            
            self.contadorColor = 0
            
            self.cambioColor()
            
            self.asignacion()

        elif len(self.prioridad) > 0:
            
            self.negociacion() 
            
            self.prioridad.clear()
            
class Coche(mesa.Agent):

    def __init__(self, unique_id, model, velocidad, color):
        
        super().__init__(unique_id, model)
        
        self.tiempoarribo = 0 
        
        self.coordenadasSemaforos = self.model.coordenadasSemaforos

        self.arribado = False 
        
        self.velocidad = velocidad
        
        self.color = color
        
        self.visited = [] 
        
        self.avanza = True 
        
        self.finalizado = False 

        self.movimientos = 0

    def calculoDistancia(self):
       
        if self.arribado == False:

            distanciaAgente = []
       
            distanciaAgente.append(self.pos)

            distancia1 = math.dist(self.pos, self.coordenadasSemaforos[0])

            distancia2 = math.dist(self.pos, self.coordenadasSemaforos[1])

            if distancia1 <= distancia2:

                self.tiempoarribo =   distancia1 / self.velocidad

            else:

                self.tiempoarribo = distancia2 / self.velocidad

    def cambioVelocidad(self): 
        nuevaVelocidad = random.randint(1,50)
        
        self.velocidad = nuevaVelocidad

    def move(self): 

        celdas = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )

        celdasVacias = 0
       
        celdasPosibles = []

        for i in celdas:

            if self.model.grid.is_cell_empty(i):
       
                celdasVacias += 1
       
                celdasPosibles.append(i)
       
            else:

                status = True
       
                contenido = self.model.grid.get_cell_list_contents([i])
                
                for j in contenido:
       
                    if type(j) == Build or type(j) == Coche:# and self.velocidad < 25: #Se agrega la velocidad
                    
                        status = False
                    
                        break

                    elif type(j) == TrafficLigth and self.arribado == True:
                   
                        status = False
                   
                        break
                        
                if status == True:
                   
                    celdasVacias += 1
                   
                    celdasPosibles.append(i)
                    
        
        if celdasVacias != 0:

            random.shuffle(celdasPosibles)
            
            for i in celdasPosibles:
            
                if i not in self.visited:
            
                    self.visited.append(i)
            
                    self.model.grid.move_agent(self, i)

    def step(self):
        
        if self.avanza == True and self.finalizado != True: 
        
            self.calculoDistancia()
        
            self.move()
        
            self.cambioVelocidad()
        
            self.movimientos += 1
        
            if not self.arribado:
        
                self.calculoDistancia()

class ModeloCamino(mesa.Model):

    def __init__(self, ancho, alto, numCochesVertical, numCochesHorizontal):
        
        self.grid = mesa.space.MultiGrid(ancho, alto, False)

        self.schedule = mesa.time.RandomActivationByType(self)

        self.numCochesVertical = numCochesVertical
        
        self.numCochesHorizontal = numCochesHorizontal
        
        self.cantidadAgentes = 0
        
        self.coordenadasSemaforos = [] 
        
        self.running = True
        
        self.promedioVelocidadesAcumuladas = []
        
        self.promedioTiemposAcumuladas = []
        
        self.tiempoActual = 0

       
        for i in range(0,2):
        
            if i != 0:
        
                Semaforos = TrafficLigth(i, self, [int(ancho/2), int(alto/2)-1])
        
                self.schedule.add(Semaforos)
        
                self.grid.place_agent(Semaforos, (int(ancho/2), int(alto/2)-1)) 
        
                self.coordenadasSemaforos.append(Semaforos.pos)
        
            else:
        
                Semaforos = TrafficLigth(i, self, [int(ancho/2)-1, int(alto/2)])
        
                self.schedule.add(Semaforos)
        
                self.grid.place_agent(Semaforos, (int(ancho/2)-1, int(alto/2))) 
        
                self.coordenadasSemaforos.append(Semaforos.pos)
        
            self.cantidadAgentes += 1

        for i in range(0, numCochesVertical):
            
            cocheVertical = Coche(i + self.cantidadAgentes, self, 22 , "orange") 
            
            self.schedule.add(cocheVertical)
            
            self.grid.place_agent(cocheVertical, (int(ancho/2), 0))
            
            cocheVertical.visited.append(cocheVertical.pos)           
            
            self.cantidadAgentes += 1

        
        for i in range(0, numCochesHorizontal):
            
            cocheHorizontal = Coche(i + numCochesVertical + self.cantidadAgentes, self, 35, "purple")
            
            self.schedule.add(cocheHorizontal)
            
            self.grid.place_agent(cocheHorizontal, (0, int(alto/2)))
            
            cocheHorizontal.visited.append(cocheHorizontal.pos)
            
            self.cantidadAgentes += 1
        
        for i in range(0,ancho):
            
            for j in range(0, alto):
            
                if (j != int(alto/2) and i != int(alto/2)) or (i != int(ancho/2) and j != int(ancho/2)) and self.grid.is_cell_empty(pos=(i,j)):
                
                    Banquetas = Build((self.cantidadAgentes+ numCochesVertical +numCochesHorizontal)*5,self,"red")
                
                    self.schedule.add(Banquetas)
                
                    self.grid.place_agent(Banquetas,(i,j))
                
                    self.cantidadAgentes += 1

        Topes = Tope((self.cantidadAgentes+numCochesHorizontal+numCochesVertical)*8,self)
        
        self.schedule.add(Topes)
        
        self.grid.place_agent(Topes,(int(ancho/2),int(alto-1)))
        
        self.cantidadAgentes += 1

        Topes = Tope((self.cantidadAgentes+numCochesHorizontal+numCochesVertical)*8,self)
        
        self.schedule.add(Topes)
        
        self.grid.place_agent(Topes,(ancho-1,int(alto/2)))

        self.datacollector = mesa.DataCollector(
            
            {
            
                "CochesArribados": ModeloCamino.cochesArribados,
            
                "PromedioVelocidades": ModeloCamino.promedioVelocidades,
            
                "PromedioDistancias": ModeloCamino.promedioTiempos,
            
                "MovimientosAgentes": ModeloCamino.movimientosAgentes,
            
            }
        )

    def step(self):

        self.schedule.step(False, True)

        self.tiempoActual += 1

        self.datacollector.collect(self)

        contador = 0

        for i in self.schedule.agents:
        
            if type(i) == Coche and i.finalizado == False:
        
                contador+=1

        if contador == 0:
        
            for i in self.schedule.agents:
        
                if type(i) == TrafficLigth:
        
                    i.contadorColor = 0
        
                    i.cambioColor()

            self.running = False

    @staticmethod
    def movimientosAgentes(model):
        
        acumulado = 0
        
        for agent in model.schedule.agents:
        
            if type(agent) == Coche:
        
                acumulado = acumulado + agent.movimientos

        return acumulado

    @staticmethod
    def cochesArribados(model):
        
        acumulado = 0
        
        for agent in model.schedule.agents:
        
            if type(agent) == Tope:
        
                acumulado = acumulado + agent.arribados

        return acumulado

    @staticmethod
    def promedioVelocidades(model):

        promedio = []

        for agent in model.schedule.agents:

            if type(agent) == Coche and agent.finalizado != True:

                promedio.append(agent.velocidad)

        if len(promedio) == 0:

            if len(model.promedioVelocidadesAcumuladas) == 0:
                return 0
            else:

                return model.promedioVelocidadesAcumuladas[-1]

        else:

            model.promedioVelocidadesAcumuladas.append(sum(promedio) / len(promedio))

            return sum(promedio) / len(promedio)
    
    @staticmethod
    def promedioTiempos(model):

        promedio = []

        for agent in model.schedule.agents:

            if type(agent) == Coche and agent.arribado != True:

                promedio.append(agent.tiempoarribo)

        if len(promedio) == 0:

            if len(model.promedioTiemposAcumuladas) == 0:
                return 0
            else:

                return model.promedioTiemposAcumuladas[-1]

        else:

            model.promedioTiemposAcumuladas.append(sum(promedio) / len(promedio))

            return sum(promedio) / len(promedio)




from mesa.visualization.UserParam import UserSettableParameter

import matplotlib.pyplot as plt

import pandas as pd

def agent_portrayal(agent):

    portrayal = {

        "Shape": "circle",

        "Filled": "true",

        "Layer": "coche",

        "Color": agent.color,

        "r": 0.5,

    }

    if type(agent) == Build:

        portrayal["Layer"] = "Build"
        
    if type(agent) == TrafficLigth:

        portrayal["Layer"] = "TrafficLigth"
    

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 750, 750)

simulation_parametrosIteraciones = {

    "numCochesVertical": UserSettableParameter(
        "slider",
        "Number of Horizontal Agents",
        50,
        1,
        50,
        1,
        description = "Elige cuantos agentes estan en la simulacion",   
    ),

    "numCochesHorizontal": UserSettableParameter(
        "slider",
        "Number of Vertical Agents",
        50,
        1,
        50,
        1,
        description = "Elige cuantos agentes estan en la simulacion",   
    ),

    "ancho": 10,

    "alto": 10,
}

movimientosGeneralesAgentes = mesa.visualization.ChartModule(

    [
        {"Label": "CochesArribados","Color": "green"},
    ],

data_collector_name='datacollector')

promedioVelocidades = mesa.visualization.ChartModule(

    [

        {"Label": "PromedioVelocidades","Color": "red"}

    ],

data_collector_name='datacollector')


server = mesa.visualization.ModularServer(
    
    ModeloCamino, [grid, movimientosGeneralesAgentes, promedioVelocidades], "Trafico Simulacion", simulation_parametrosIteraciones

)

server.port = 8521

server.launch()