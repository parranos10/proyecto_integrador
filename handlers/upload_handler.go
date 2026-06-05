package handlers

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

func Upload(w http.ResponseWriter, r *http.Request) {

	if r.Method != http.MethodPost {
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		return
	}

	r.ParseMultipartForm(10 << 20)

	file, handler, err := r.FormFile("image")
	if err != nil {
		http.Error(w, "Error al obtener la imagen", http.StatusBadRequest)
		return
	}
	defer file.Close()

	extension := filepath.Ext(handler.Filename)
	uniqueName := fmt.Sprintf("%d%s", time.Now().UnixNano(), extension)
	savePath := filepath.Join("./uploads", uniqueName)

	dst, err := os.Create(savePath)
	if err != nil {
		http.Error(w, "Error al guardar la imagen", http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, "Error al escribir el archivo", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"message": "Imagen subida con éxito", "filename": "%s"}`, uniqueName)
}

func Home(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"message": "Servidor Core de Gestión de Imágenes en Go activo"}`)
}

func GetImages(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		return
	}

	files, err := os.ReadDir("./uploads")
	if err != nil {
		http.Error(w, "Error al leer la carpeta de imágenes", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	fmt.Fprintf(w, `{"images": [`)
	for i, file := range files {
		if !file.IsDir() {
			fmt.Fprintf(w, `"%s"`, file.Name())
			if i < len(files)-1 {
				fmt.Fprintf(w, ", ")
			}
		}
	}
	fmt.Fprintf(w, `]}`)
}
