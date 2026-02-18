# blog de notas con flet GG
# flet version : 0.28.3

import flet as ft

def app(page: ft.Page):
    page.title = "Bloc de notas"
    page.window.maximized = True
    page.auto_scroll = True
    page.window.icon = "notas.ico"

    archivo_actual = {"ruta": None, "nombre": None}

    # --- Cargar archivo ---
    def cargar_file(e: ft.FilePickerResultEvent):
        if e.files:
            archivo = e.files[0]
            archivo_actual["ruta"] = archivo.path
            archivo_actual["nombre"] = archivo.name

            try:
                with open(archivo.path, "r", encoding="utf-8") as f:
                    entrada_escribir.value = f.read()
            except:
                entrada_escribir.value = f"Error al cargar archivo {archivo.path}"

            page.title = f"Bloc de notas - {archivo.name}"
            page.update()

    # --- Guardar ---
    def guardar_archivo(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(entrada_escribir.value)
                page.title = f"Bloc de notas - {e.path.split('/')[-1]}"
            except Exception as ex:
                entrada_escribir.value = f"Error al guardar archivo: {ex}"
            page.update()

    # FilePickers
    picker_cargar = ft.FilePicker(on_result=cargar_file)
    picker_guardar = ft.FilePicker(on_result=guardar_archivo)

    page.overlay.append(picker_cargar)
    page.overlay.append(picker_guardar)

    # Función para cerrar el diálogo
    def cerrar_dialogo(e):
        cuadro_dialogo.open = False
        page.update()

    # Función para abrir el diálogo
    def abrir_dialogo(e):
        cuadro_dialogo.open = True
        page.update()

    cuadro_dialogo = ft.AlertDialog(
        title=ft.Text("Información del Bloc de notas"),
        content=ft.Text("""Bloc de notas con flet (adminte todo html,txt,md,py,cpp,etc)
                        ,\nimplementacion de plugins y busqueda de palabras\nVersión 1.0"""),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo)
        ],
        open=False
    )
    
    # Agregar el diálogo al overlay
    page.overlay.append(cuadro_dialogo)

    informacion = ft.IconButton(
        icon=ft.Icons.INFO_OUTLINED,
        tooltip="Información",
        on_click=abrir_dialogo
    )

    # Botones
    guardar = ft.IconButton(
        icon=ft.Icons.SAVE,
        tooltip="Guardar archivo",
        on_click=lambda _: picker_guardar.save_file(
            file_name="nuevo_archivo.txt"
        )
    )

    cargar = ft.IconButton(
        icon=ft.Icons.UPLOAD_FILE_OUTLINED,
        tooltip="Abrir archivo",
        on_click=lambda _: picker_cargar.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.ANY
        )
    )

    salir = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        tooltip="Salir",
        on_click=lambda _: page.window.close()
    )

    fila = ft.Row([guardar, cargar, salir,informacion], spacing=20)

    global entrada_escribir
    entrada_escribir = ft.TextField(
        multiline=True,
        expand=True,
        border=ft.InputBorder.NONE,
        hint_text="Escribe aquí..."
    )



    page.add(fila, entrada_escribir)

ft.app(target=app,assets_dir="assets",view=ft.FLET_APP)
