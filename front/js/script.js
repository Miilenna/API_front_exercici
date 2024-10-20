document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch("http://localhost:8000/alumne/list")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                //Nom de l'alumne
                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                // Repetir per tots els altres camps restants que retorna l'endpoint
                
                //Ciclo
                const CicleCell = document.createElement("td");
                CicleCell.textContent = alumne.Cicle;
                row.appendChild(CicleCell);

                //Curso
                const CursCell = document.createElement("td");
                CursCell.textContent = alumne.Curs;
                row.appendChild(CursCell);

                //Grupo
                const GrupCell = document.createElement("td");
                GrupCell.textContent = alumne.Grup;
                row.appendChild(GrupCell);

                //Nombre del aula
                const DescAulaCell = document.createElement("td");
                DescAulaCell.textContent = alumne.DescAula;
                row.appendChild(DescAulaCell);
                

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});