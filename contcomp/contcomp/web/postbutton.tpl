<!DOCTYPE html>
	<html>
	<header>

	</header>
	<body>
		<button id="fetchdata"> BUTTON</button>
	</body>

		<script type="text/javascript">
			document.getElementById("fetchdata").addEventListener('click', fetchdata);
			function fetchdata(){
				fetch('../testPOST', {
					method: 'POST',
					body:JSON.stringify({'item1':'field1', 'item2':'field2'})
				}).then((res) => res.json())
				.then((data) => console.log(data))
				.catch((err)=>console.log(err))
			};
		</script>
	</html>