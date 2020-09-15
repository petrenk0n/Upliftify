// Scroll to a div after clicking the button
document.getElementById('{{ scroll }}').scrollIntoView();

<script src="../static/webcam.js"></script>

// Webcam.js code to display the webcam viewfinder
Webcam.attach('#my_camera');
function take_snapshot() {
	Webcam.snap( function(data_uri) {
		document.getElementById('my_result').innerHTML = '<img src="'+data_uri+'"/>';
        // Sending the image to flask
        $.ajax({
			type: "GET",
			data: "myimage=" + encodeURIComponent(data_uri),
			url: "/upload",
			contentType: false,
			processData: false,
			success: function (jsonresult) {
                console.log("Success");
			}
		});
	});
}

// Toggle visibility of picture taken div
function myFunction() {
    var x = document.getElementById("picture-taken");
    if (x.style.display === "none") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
  }

// Toggle visibility of identification div
function myFunction2() {
    var x = document.getElementById("iden-done");
    if (x.style.display === "none") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}