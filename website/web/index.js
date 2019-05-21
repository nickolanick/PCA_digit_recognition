import "./static/css/main.scss";
// import "./static/img/Placeholder.jpg" ;

let linearAlgebra = require('linear-algebra')(),
    Matrix = linearAlgebra.Matrix;


const add_ftr = (ftr_name, matrix, parent) => {
    let regular_matrix = document.createElement('div');
    let header = document.createElement('h1');
    header.innerHTML = ftr_name
    header.className = "matrix__header"

    regular_matrix.className = "matrix"
    let n = Math.sqrt(matrix.length)
    regular_matrix.style.width = `${n * 70}px`;
    // while (regular_matrix.firstChild) {
    //     regular_matrix.removeChild(regular_matrix.firstChild);
    // }
    for (let i = 0; i < matrix.length; i++) {
        let inner_digit = document.createElement('div');
        inner_digit.innerHTML = matrix[i];
        inner_digit.className = 'matrix__item'
        regular_matrix.appendChild(inner_digit);
    }
    parent.appendChild(header);
    parent.appendChild(regular_matrix)
};
const convert_matrix = (matrix) => matrix.data.join().split(",")
const place_matrix = digits => {
    let results = document.getElementsByClassName("results_block")[0];
    let n = Math.sqrt(digits.length)
    let digits_great = [];
    for (let ind = 0; ind < n; ind++) {
        digits_great.push(digits.slice(ind * n, (ind + 1) * n))
    }
    let mtr_regular = new Matrix(digits_great);

    let mtr_transpose = new Matrix(digits_great);
    let mtr_square = new Matrix(digits_great);

    mtr_transpose = mtr_transpose.trans();
    mtr_square = mtr_square.dot(mtr_square);


    add_ftr("Your Matrix", convert_matrix(mtr_regular), results);
    add_ftr("Transpose", convert_matrix(mtr_transpose), results);
    add_ftr("Squared", convert_matrix(mtr_square), results);


};

const uploadFile = () => {
    let file = document.getElementById("matrix_image_insert");

    console.log(file.files[0]);
    fetch('/getMatrix', {
        method: 'post',
        body: file.files[0]
    }).then(response => {
        return response.json();
    }).then(data => {

        place_matrix(data.digits);
        // document.getElementById("image_inserted").src = "data:image/png;base64," + data.bytes;

        console.log("data", data)
    });
}

const readURL = () => {
    let input = document.getElementById("matrix_image_insert");
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = (e) => {
            document.getElementById("image_inserted").setAttribute('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
};

document.getElementById("matrix_image_insert").addEventListener('change', () => {

    console.log("inserted");
    readURL();
});


(() => {

    document.getElementById("uploadFile").addEventListener('click', uploadFile)

})()

