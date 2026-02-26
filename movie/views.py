import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie




def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name':'Jeronimo Rodriguez'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html', {})

def signup(request):
    email = request.GET.get("email")
    return render(request, 'signup.html', {'email':email})
    
def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}

    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras por año
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png)
    graphic_year = graphic_year.decode('utf-8')

    # === GRÁFICA POR GÉNERO ===
    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}

    # Contar películas por primer género
    for movie in all_movies:
        if movie.genre:
            # Obtener el primer género (separado por comas)
            first_genre = movie.genre.split(',')[0].strip()
            if first_genre:
                if first_genre in movie_counts_by_genre:
                    movie_counts_by_genre[first_genre] += 1
                else:
                    movie_counts_by_genre[first_genre] = 1
        else:
            if "None" in movie_counts_by_genre:
                movie_counts_by_genre["None"] += 1
            else:
                movie_counts_by_genre["None"] = 1

    # Posiciones de las barras para género
    bar_positions_genre = range(len(movie_counts_by_genre))

    # Crear la gráfica de barras por género
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center', color='orange')

    # Personalizar la gráfica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en un objeto BytesIO
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre)
    graphic_genre = graphic_genre.decode('utf-8')

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })