<div class="carousel relative shadow-2xl bg-white">
    <div class="carousel-inner relative overflow-hidden w-full">
      <!--Slide 1-->
      <input
        class="carousel-open"
        type="radio"
        id="carousel-1"
        name="carousel"
        aria-hidden="true"
        hidden=""
        checked="checked"
      />
      <div class="carousel-item absolute opacity-0" style="height: 50vh">
        <div
          class="block h-full w-full bg-indigo-500 text-white text-5xl text-center"
        >
          Slide 1
        </div>
      </div>

      <!--Custome Slide 1-->
      <input
        class="carousel-open"
        type="radio"
        id="carousel-{{sl.id}}"
        name="carousel"
        aria-hidden="true"
        hidden=""
      />
      <div class="carousel-item absolute opacity-100" style="height: 50vh">
        <img src="/{{sl.img}}" />
        <div
          class="block h-full w-full bg-green-500 text-white text-5xl text-center"
          style="opacity: 2"
        >
          Slide 3
        </div>
      </div>


      {% for sld in slides %}
        <!--Custome Slide 1-->
        <input
          class="carousel-open"
          type="radio"
          id="carousel-{{sld.id}}"
          name="carousel"
          aria-hidden="true"
          hidden=""
        />
        <div class="carousel-item absolute opacity-100" style="height: 50vh">
          <img src="/{{sld.img}}" width="100%" height="400" />
          <div
            class="block h-full w-full bg-green-500 text-white text-5xl text-center"
            style="opacity: 2"
          >
            {{sld.text}}
          </div>
        </div>
      {% endfor %}



      <!-- Add additional indicators for each slide-->
      <ol class="carousel-indicators">
        <li class="inline-block mr-3">
          <label
            for="carousel-1"
            class="carousel-bullet cursor-pointer block text-4xl text-white hover:text-blue-700"
            >•</label
          >
        </li>

        <li class="inline-block mr-3">
          <label
            for="carousel-{{sl.id}}"
            class="carousel-bullet cursor-pointer block text-4xl text-white hover:text-blue-700"
            >{{sl.text}}</label
          >
        </li>

        {% for sld in slides %}
          <li class="inline-block mr-3">
            <label
              for="carousel-{{sld.id}}"
              class="carousel-bullet cursor-pointer block text-4xl text-white hover:text-blue-700"
              >{{sld.id}}</label
            >
          </li>

        {% endfor %}


      </ol>
    </div>
  </div>

  {{sl}} 
  {% comment %} manage slides link {% endcomment %}
  {% if request.user.is_superuser %}
    <div>
      <a href="{% url 'shop:slide-create' pk=request.user.id %}">Manage slides</a>
    </div>
  {% endif %} 
  
  {% for sld in slides %}
  <img src = "/{{sld.img}}"/>
  {{sld.text}} {{sld.id}}

  
  {% endfor %}
  