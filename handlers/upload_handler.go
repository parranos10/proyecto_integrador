package handlers

import (
	"fmt"
	"net/http"
)

func UploadImage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Subir imagen")
}
