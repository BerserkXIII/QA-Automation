# ════════════════════════════════════════════════════════════════════
# EJEMPLO RESUELTO: Tests de _evento_1
# ════════════════════════════════════════════════════════════════════
"""
Este archivo muestra cómo implementar tests reales basados en 
ESPECIFICACION_EVENTS.md (Tests E1.1 a E1.5).

Úsalo como REFERENCIA para escribir tus propios tests.
NO EDITES este archivo — es una guía de lectura.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestEvento1:
    """
    Agrupa todos los tests de _evento_1 bajo una clase.
    Ventaja: organización clara + podemos usar fixtures a nivel clase.
    """
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST E1.1: Rama ABRIR → POCIÓN
    # ═══════════════════════════════════════════════════════════════════
    def test_evento_1_abrir_cofre_pocion(self, personaje_base, mock_leer_input):
        """
        Spec: Test E1.1 — rama ABRIR cofre → resultado aleatoriedad → POCIÓN
        
        Escenario:
        - Jugador abre cofre (responde "s")
        - Random elige "poción" 
        → Retorna {\"pociones\": 1}
        
        Inyecciones necesarias:
        - leer_input() para simular respuesta jugador
        - random.choice() para determinismo en rama
        """
        
        # ═════════════════════════════════════════════════════════════
        # ARRANGE
        # ═════════════════════════════════════════════════════════════
        personaje = personaje_base.copy()
        
        # Mock leer_input para retornar "s" (abrir cofre)
        mock_leer_input.return_value = "s"
        
        # ═════════════════════════════════════════════════════════════
        # ACT
        # ═════════════════════════════════════════════════════════════
        
        # Simulamos _evento_1 con el mock de random
        with patch("random.choice") as mock_random_choice:
            # Forzamos que random.choice retorne "poción"
            mock_random_choice.return_value = "poción"
            
            # Inyectamos dependencias: en código real, esto se hace via
            # módulo events con narrar(), alerta(), etc. inyectadas
            with patch("modules.events.leer_input", mock_leer_input):
                # Importar y ejecutar (en test real, importarías desde TLDRDC_Prueba1)
                resultado = self._evento_1_simulado(personaje, mock_leer_input, mock_random_choice)
        
        # ═════════════════════════════════════════════════════════════
        # ASSERT
        # ═════════════════════════════════════════════════════════════
        assert resultado == {"pociones": 1}, \
            f"Esperado {{\"pociones\": 1}}, obtenido {resultado}"
        # Verificamos que leer_input fue llamado (preguntó al jugador)
        mock_leer_input.assert_called()
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST E1.2: Rama ABRIR → CORTE (daño)
    # ═══════════════════════════════════════════════════════════════════
    def test_evento_1_abrir_cofre_corte(self, personaje_base, mock_leer_input):
        """
        Spec: Test E1.2 — rama ABRIR → CORTE
        
        Escenario:
        - Jugador abre cofre ("s")
        - Random elige "corte" (pone trampa)
        → Retorna {\"vida\": -1}
        """
        
        # ARRANGE
        personaje = personaje_base.copy()
        mock_leer_input.return_value = "s"
        
        # ACT
        with patch("random.choice") as mock_random:
            mock_random.return_value = "corte"
            
            with patch("modules.events.leer_input", mock_leer_input):
                resultado = self._evento_1_simulado(personaje, mock_leer_input, mock_random)
        
        # ASSERT
        assert resultado == {"vida": -1}
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST E1.3: Rama NO ABRIR → SOMBRA (combate)
    # ═══════════════════════════════════════════════════════════════════
    def test_evento_1_no_abrir_combate_sombra(self, personaje_base, mock_leer_input, mock_combate):
        """
        Spec: Test E1.3 — rama NO ABRIR → SOMBRA (peligro)
        
        Escenario:
        - Jugador NO abre cofre ("n")
        - Random elige "sombra"
        → Llama combate(personaje, \"Sombra tenebrosa\")
        → Retorna {}
        """
        
        # ARRANGE
        personaje = personaje_base.copy()
        mock_leer_input.return_value = "n"  # No abrir
        
        # ACT
        with patch("random.choices") as mock_random_choices:
            mock_random_choices.return_value = ["sombra"]  # random.choices retorna lista
            
            with patch("modules.events.leer_input", mock_leer_input):
                with patch("modules.events.combate", mock_combate):
                    resultado = self._evento_1_simulado_no_abrir(
                        personaje, mock_leer_input, mock_random_choices, mock_combate
                    )
        
        # ASSERT
        assert resultado == {}
        # Verificamos que combate fue llamado
        mock_combate.assert_called()
        # En test real verificarías que fue llamado con "Sombra tenebrosa"
        call_args = mock_combate.call_args
        assert call_args is not None
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST E1.4: Input inválido (loop reintenta)
    # ═══════════════════════════════════════════════════════════════════
    def test_evento_1_rechaza_input_invalido(self, personaje_base, mock_leer_input, mock_alerta):
        """
        Spec: Test E1.4 — entrada inválida se rechaza
        
        Escenario:
        - Jugador envía "xyz" (inválido)
        - Loop reintenta, pide de nuevo
        - Jugador envía "s" (válido)
        - Evento procesa correctamente
        """
        
        # ARRANGE
        personaje = personaje_base.copy()
        
        # Mock para retornar entrada inválida primero, luego válida
        mock_leer_input.side_effect = ["xyz", "s"]  # 1er intento: inválido, 2o: válido
        
        # ACT
        with patch("random.choice") as mock_random:
            mock_random.return_value = "poción"
            
            with patch("modules.events.leer_input", mock_leer_input):
                with patch("modules.events.alerta", mock_alerta):
                    resultado = self._evento_1_simulado(personaje, mock_leer_input, mock_random)
        
        # ASSERT
        # alerta fue llamado (rechazó input inválido)
        mock_alerta.assert_called()
        # Evento se procesó correctamente tras reintentos
        assert resultado == {"pociones": 1}
        # leer_input fue llamado 2 veces (inválido + válido)
        assert mock_leer_input.call_count == 2
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST E1.5: Rama VACÍO (sin treasure)
    # ═══════════════════════════════════════════════════════════════════
    def test_evento_1_abrir_cofre_vacio(self, personaje_base, mock_leer_input):
        """
        Spec: Test E1.5 — rama ABRIR → VACÍO
        
        Escenario:
        - Jugador abre cofre ("s")
        - Random elige "vacío"
        → Retorna {} (sin cambios)
        """
        
        # ARRANGE
        personaje = personaje_base.copy()
        mock_leer_input.return_value = "s"
        
        # ACT
        with patch("random.choice") as mock_random:
            mock_random.return_value = "vacío"
            
            with patch("modules.events.leer_input", mock_leer_input):
                resultado = self._evento_1_simulado(personaje, mock_leer_input, mock_random)
        
        # ASSERT
        assert resultado == {}
    
    # ═════════════════════════════════════════════════════════════════
    # HELPERS (Simulaciones de _evento_1)
    # ═════════════════════════════════════════════════════════════════
    
    def _evento_1_simulado(self, personaje, mock_leer_input, mock_random):
        """
        Simula el flujo de _evento_1 rama ABRIR.
        En test real, importarías _evento_1 desde modules.events.
        
        Este es solo una demostración del flujo lógico.
        """
        while True:
            resp = mock_leer_input()
            
            if resp in ["s", "si"]:
                cofre = mock_random(["poción", "vacío", "corte"])
                
                if cofre == "poción":
                    return {"pociones": 1}
                elif cofre == "corte":
                    return {"vida": -1}
                else:  # vacío
                    return {}
            elif resp in ["n", "no"]:
                # Rama NO ABRIR (ver método siguiente)
                return {}
            else:
                # Entrada inválida — reintenta
                # En código real: alerta("Respuesta no válida")
                continue
    
    def _evento_1_simulado_no_abrir(self, personaje, mock_leer_input, mock_random_choices, mock_combate):
        """
        Simula el flujo de _evento_1 rama NO ABRIR.
        """
        resp = mock_leer_input()
        
        if resp in ["n", "no"]:
            accion = mock_random_choices(["sombra", "mutilado", "escape"], weights=[33, 33, 34], k=1)[0]
            
            if accion == "sombra":
                mock_combate(personaje, "Sombra tenebrosa")
            elif accion == "mutilado":
                mock_combate(personaje, "Maniaco Mutilado")
            else:  # escape
                pass
            
            return {}
        
        return {}


# ════════════════════════════════════════════════════════════════════
# NOTAS PARA APRENDER
# ════════════════════════════════════════════════════════════════════

"""
🎯 PUNTOS CLAVE DE ESTE EJEMPLO:

1. ESTRUCTURA AAA
   - ARRANGE: Preparar datos y mocks
   - ACT: Ejecutar función con inyecciones
   - ASSERT: Verificar resultado

2. MOCKING
   - patch() para simular funciones externas
   - Mock.side_effect para múltiples retornos (entradas del usuario)
   - Mock.assert_called() para verificar llamadas

3. PARAMETRIZACIÓN
   - Cada test cubre UNA rama (poción, corte, combate, etc.)
   - Tests independientes: no dependen uno de otro
   - Fácil de entender: nombre claro + spec clara

4. FIXTURES
   - personaje_base: Reutilizable para todos
   - mock_leer_input: Inyectado desde conftest.py
   - mock_alerta, mock_combate: Mockeos separados

5. CÓDIGO REAL vs SIMULACIÓN
   - Este archivo usa _evento_1_simulado (demo)
   - En test real: from modules.events import _evento_1
   - Luego: resultado = _evento_1(personaje)
   - Los mocks se inyectan en el módulo via patch()

🚀 PRÓXIMOS PASOS:
   1. Lee la especificación (ESPECIFICACION_EVENTS.md)
   2. Copia este archivo como plantilla
   3. Reemplaza _evento_1_simulado con import real
   4. Ejecuta: pytest -v tests/unit/test_ejemplo_evento1.py
   5. ¡Éxito! ✅
"""
