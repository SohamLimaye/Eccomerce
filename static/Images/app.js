$(document).ready(function () {
    // Add Product Form Submission
    $('#addProductForm').submit(function (event) {
        event.preventDefault();

        var productName = $('#productName').val();
        var price = $('#price').val();
        var quantity = $('#quantity').val();

        $.ajax({
            url: '/add_product',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: productName,
                price: parseInt(price),
                quantity: parseInt(quantity)
            }),
            success: function (response) {
                alert(response.message);
                $('#addProductForm')[0].reset();
            },
            error: function (xhr, status, error) {
                alert(JSON.parse(xhr.responseText).error);
            }
        });
    });

    // View Cart Button Click
    $('#viewCartBtn').click(function () {
        var userId = prompt('Enter User ID:');
        if (userId) {
            $.ajax({
                url: '/cart/view',
                type: 'GET',
                contentType: 'application/json',
                data: { user_id: userId },
                success: function (response) {
                    var cartItems = '';
                    response.cart.products.forEach(function (product) {
                        cartItems += `<tr>
                            <td>${product.product.name}</td>
                            <td>${product.product.price}</td>
                            <td>${product.quantity}</td>
                        </tr>`;
                    });
                    $('#cartItems').html(cartItems);
                    $('#totalAmount').text(response.cart.total_amount);
                },
                error: function (xhr, status, error) {
                    alert(JSON.parse(xhr.responseText).error);
                }
            });
        }
    });

    // Delete Cart Button Click
    $('#deleteCartBtn').click(function () {
        var userId = prompt('Enter User ID:');
        if (userId) {
            $.ajax({
                url: '/cart/delete',
                type: 'DELETE',
                contentType: 'application/json',
                data: JSON.stringify({ user_id: userId }),
                success: function (response) {
                    alert(response.message);
                },
                error: function (xhr, status, error) {
                    alert(JSON.parse(xhr.responseText).error);
                }
            });
        }
    });
});
