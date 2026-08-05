# Análisis QA SauceDemo

## Descripción
Este documento recoge el análisis manual de los aprendizajes y observaciones obtenidos durante el ejercicio de automatización en SauceDemo. No se trata de un bug crítico, sino de la experiencia de aprendizaje en la estructuración de pruebas y en el uso de POM.

*Fecha de última actualización:* 05/08/2026

## Contexto
SauceDemo fue el primer ejercicio práctico en el que trabajé con pruebas web automatizadas. La experiencia se centró en organizar los tests mediante Page Object Model, evitar dependencias directas entre locators y scripts de prueba, y encontrar un flujo estable para login, carrito y checkout.

## Aprendizajes clave
- **Estructura POM**: Aprendí a separar responsabilidades entre páginas (`home_page`, `login_page`, `inventory_page`, `cart_page`) y a mantener los tests limpios con acciones reutilizables.
- **Locators correctos**: Detecté que usar selectores robustos evita fragilidad. Los tests funcionan mejor cuando los locators se mantienen en los page objects y no se repiten en cada test.
- **Tests más cortos**: Al principio escribí escenarios más largos y menos mantenibles. La lección fue dividir en tests pequeños y mediados, cada uno con un objetivo claro.
- **Validaciones explícitas**: Verificar la URL esperada y la presencia de elementos relevantes en cada paso ayuda a detectar fallos de navegación antes de que el test siga.

Ejemplo práctico:
```python
class LoginPage:
    def hacer_login(self, usuario, contraseña):
        self.page.locator("[data-test='username']").fill(usuario)
        self.page.locator("[data-test='password']").fill(contraseña)
        self.page.locator("[data-test='login-button']").click()

    def verificar_login_fallido(self, mensaje_esperado):
        expect(self.page.locator("[data-test='error']")).to_have_text(mensaje_esperado)
```

Este patrón separa el detalle del locator de la lógica del test, haciendo más claro el propósito de cada caso.

## Observaciones de calidad
- **Login correcto**: Fue el flujo más estable. Usar usuarios válidos y checks de URL garantizó que el paso inicial estuviera bien cubierto.
- **Login incorrecto**: Comprobé mensajes de error y validé que la aplicación no avanza con credenciales inválidas.
- **Carrito**: Añadir y eliminar productos resultó útil para comprender cómo se comporta el DOM con cambios dinámicos.
- **Checkout**: El checkout completo es un caso integral donde se valida navegación, datos de pago y confirmación final.
- **Carrito vacío**: Identifiqué un edge case interesante: la aplicación permite intentar checkout con carrito vacío. Esto es un comportamiento relevante a documentar como observación de producto.

## Lecciones aprendidas
- No todos los ejercicios necesitan un bug. A veces el valor está en documentar cómo se aprendió a escribir pruebas más limpias y robustas.
- El primer ejercicio es ideal para practicar POM y para distinguir entre: validar funcionalidad versus validar estructura de pruebas.
- Mantener los tests en una capa de negocio y los locators en los page objects hace que el código sea más fácil de mantener y menos propenso a roturas cuando cambia la UI.

## Recomendaciones para el futuro
- Usar `pytest.mark.parametrize` para cubrir variantes de login y filtros sin repetir código.
- Añadir casos negativos adicionales sobre el carrito y la navegación lateral, especialmente cuando el flujo involucra cambios de URL.
- Documentar los elementos de UI más frágiles en los page objects para facilitar su mantenimiento cuando la aplicación sufra cambios.
