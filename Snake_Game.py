import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
TAMAÑO_CELDA = 20

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
GRIS = (128, 128, 128)

FPS = 10

class Snake:
    def __init__(self):
    
     # Posición inicial de la serpiente (centro de la pantalla)
        self.posiciones = [(ANCHO // 2, ALTO // 2)]
        self.direccion = (TAMAÑO_CELDA, 0)  # Inicialmente moviéndose hacia la derecha
        self.crecer = False
        
    def mover(self):
        # Obtener la cabeza actual
        cabeza = self.posiciones[0]
        # Calcular nueva posición de la cabeza
        nueva_cabeza = (cabeza[0] + self.direccion[0], cabeza[1] + self.direccion[1])
        
        # Agregar nueva cabeza
        self.posiciones.insert(0, nueva_cabeza)
        
        # Si no debe crecer, eliminar la cola
        if not self.crecer:
            self.posiciones.pop()
        else:
            self.crecer = False
    
    def cambiar_direccion(self, nueva_direccion):
        # Evitar que la serpiente se mueva en dirección opuesta
        if (nueva_direccion[0] * -1, nueva_direccion[1] * -1) != self.direccion:
            self.direccion = nueva_direccion
    
    def comer(self):
        self.crecer = True
    
    def colision_consigo_misma(self):
        cabeza = self.posiciones[0]
        return cabeza in self.posiciones[1:]
    
    def colision_bordes(self):
        cabeza = self.posiciones[0]
        return (cabeza[0] < 0 or cabeza[0] >= ANCHO or 
                cabeza[1] < 0 or cabeza[1] >= ALTO)
    
    def dibujar(self, pantalla):
        for i, posicion in enumerate(self.posiciones):
            rect = pygame.Rect(posicion[0], posicion[1], TAMAÑO_CELDA, TAMAÑO_CELDA)
            # Cabeza en color diferente
            if i == 0:
                pygame.draw.rect(pantalla, AZUL, rect)
            else:
                pygame.draw.rect(pantalla, VERDE, rect)
            pygame.draw.rect(pantalla, BLANCO, rect, 1)

class Manzana:
    def __init__(self):
        self.posicion = self.generar_posicion()
    
    def generar_posicion(self):
        x = random.randint(0, (ANCHO - TAMAÑO_CELDA) // TAMAÑO_CELDA) * TAMAÑO_CELDA
        y = random.randint(0, (ALTO - TAMAÑO_CELDA) // TAMAÑO_CELDA) * TAMAÑO_CELDA
        return (x, y)
    
    def reposicionar(self, posiciones_serpiente):
        while True:
            self.posicion = self.generar_posicion()
            if self.posicion not in posiciones_serpiente:
                break
    
    def dibujar(self, pantalla):
        rect = pygame.Rect(self.posicion[0], self.posicion[1], TAMAÑO_CELDA, TAMAÑO_CELDA)
        pygame.draw.rect(pantalla, ROJO, rect)
        pygame.draw.rect(pantalla, BLANCO, rect, 1)

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Snake - Proyecto Final")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 36)
        self.reiniciar()
    
    def reiniciar(self):
        self.serpiente = Snake()
        self.manzana = Manzana()
        self.puntuacion = 0
        self.juego_terminado = False
        self.velocidad = FPS
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if not self.juego_terminado:
                    if evento.key == pygame.K_UP:
                        self.serpiente.cambiar_direccion((0, -TAMAÑO_CELDA))
                    elif evento.key == pygame.K_DOWN:
                        self.serpiente.cambiar_direccion((0, TAMAÑO_CELDA))
                    elif evento.key == pygame.K_LEFT:
                        self.serpiente.cambiar_direccion((-TAMAÑO_CELDA, 0))
                    elif evento.key == pygame.K_RIGHT:
                        self.serpiente.cambiar_direccion((TAMAÑO_CELDA, 0))
                else:
                    if evento.key == pygame.K_SPACE:
                        self.reiniciar()
                    elif evento.key == pygame.K_ESCAPE:
                        return False
        return True
    
    def actualizar(self):
        if not self.juego_terminado:
            self.serpiente.mover()
            
            # Verificar colisiones
            if (self.serpiente.colision_bordes() or 
                self.serpiente.colision_consigo_misma()):
                self.juego_terminado = True
                return
            
            # Verificar si comió la manzana
            if self.serpiente.posiciones[0] == self.manzana.posicion:
                self.serpiente.comer()
                self.manzana.reposicionar(self.serpiente.posiciones)
                self.puntuacion += 10
                
                # Velocidad progresiva
                if self.puntuacion % 30 == 0:
                    self.velocidad += 1
    
    def dibujar(self):
        self.pantalla.fill(NEGRO)
        
        # Dibujar bordes
        pygame.draw.rect(self.pantalla, GRIS, (0, 0, ANCHO, ALTO), 2)
        
        if not self.juego_terminado:
            self.serpiente.dibujar(self.pantalla)
            self.manzana.dibujar(self.pantalla)
        
        # Mostrar puntuación
        texto_puntuacion = self.fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto_puntuacion, (10, 10))
        
        # Mostrar velocidad
        texto_velocidad = self.fuente.render(f"Velocidad: {self.velocidad}", True, BLANCO)
        self.pantalla.blit(texto_velocidad, (10, 50))
        
        if self.juego_terminado:
            # Mensaje cuando pierdes el juego
            texto_game_over = self.fuente.render("¡Perdiste!", True, ROJO)
            rect_game_over = texto_game_over.get_rect(center=(ANCHO//2, ALTO//2 - 30))
            self.pantalla.blit(texto_game_over, rect_game_over)
            
            texto_puntuacion_final = self.fuente.render(f"Puntuación Final: {self.puntuacion}", True, BLANCO)
            rect_puntuacion = texto_puntuacion_final.get_rect(center=(ANCHO//2, ALTO//2))
            self.pantalla.blit(texto_puntuacion_final, rect_puntuacion)
            
            texto_reiniciar = self.fuente.render("Presiona ESPACIO para reiniciar o ESC para salir", True, BLANCO)
            rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO//2, ALTO//2 + 40))
            self.pantalla.blit(texto_reiniciar, rect_reiniciar)
        
        pygame.display.flip()
    
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(self.velocidad)
        
        pygame.quit()
        sys.exit()

def main():
    juego = Juego()
    juego.ejecutar()

if __name__ == "__main__":
    main()