// var all_prods = `{% for prd in object_list %}{{prd.id}},{{prd.name}},{{prd.price}},{{prd.stock}},{% for cat in prd.category.all %}{{cat}},{% endfor %} {% endfor %}` { % comment % }
// console.log(all_prods)
// all_prods = all_prods.split(" ")
// all_prods = all_prods.slice(0, all_prods.length - 1)
// console.log(all_prods)
// for (var i in all_prods) {
//     console.log(i)
//     all_prods[i] = all_prods[i].split(",")
//     all_prods[i] = all_prods[i].slice(0, all_prods[i].length - 1)

// }
// console.log(all_prods)

// var ind = 0;

// function myFunction(e) {
//     var prd = all_prods[ind]
//     var id = prd[0]
//     var name = prd[1]
//     var price = prd[2]
//     var stock = prd[3]
//     var cat_prd = prd.slice(4, prd.length)

//     var card_div = document.getElementById("product-cards")

//     var new_card = `
//     <div class="lg:w-1/4 md:w-1/2 p-4 w-full">
//       <a
//         class="block relative h-48 rounded overflow-hidden"
//         href="{% url 'shop:product_update' ${toString(id)} %}"
//       >
//         <img
//           alt="ecommerce"
//           class="object-cover object-center w-full h-full block"
//           src="https://dummyimage.com/420x260"
//         />
//       </a>
//       <div class="mt-4">
//         <h3 class="text-gray-500 text-xs tracking-widest title-font mb-1">
//           {% if ${stock} > 0 %}
//           <p>
//             In stock
//             <span
//               class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-green-100 bg-green-600 rounded-full"
//               >${stock}</span
//             >
//           </p>
//           {% else %}
//           <p>
//             <span
//               class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 bg-red-600 rounded-full"
//               >Out of stock</span
//             >
//           </p>
//           {% endif %}
//         </h3>
//         <h2 class="text-gray-900 title-font text-lg font-medium">
//           ${name}
//         </h2>
//         <p class="mt-1">Rs. {{prod.price}}</p>
//         <p class = "flex prod-cat" style = "border:5px solid Black">

//         </p>
//         <br>

//         {% if user.shop == prod.shop %}
//         <button
//           class="ml-right text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded"

//         >
//         <a href = "{% url "shop:product_update" ${id} %}">
//           Update
//         </a>
//         </button>
//         <button
//           class="ml-right text-white bg-red-600 border-y-200 py-2 px-6 focus:outline-none hover:bg-red-700 rounded"
//           style="float: right"
//         >
//           <a href="{% url 'shop:product_delete' ${id} %}">
//             <p class="mt-1">Delete</p>
//           </a>
//         </button>
//         {% else %}
//         {% endif %}

//       </div>
//     </div>
//         `
//     console.log(new_card)

//     // card_div.appendChild(new_card)
// }