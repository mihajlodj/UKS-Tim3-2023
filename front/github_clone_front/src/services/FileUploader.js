// import api from '../api'

function fileToBase64(fileUrl) {
	return new Promise((resolve, reject) => {
		const xhr = new XMLHttpRequest();
		xhr.onload = function () {
			const reader = new FileReader();
			reader.onloadend = function () {
				resolve(reader.result);
			}
			reader.onerror = function (error) {
				reject(error);
			}
			reader.readAsDataURL(xhr.response);
		};
		xhr.onerror = function (error) {
			reject(error);
		};
		xhr.open('GET', fileUrl);
		xhr.responseType = 'blob';
		xhr.send();
	});
}


// owner, repoName, message, branch
const uploadFiles = (files, data) => {
	console.log("IN UPLOADER");
	let fileData = []
	for (let file of files) {
		console.log(file);
		fileToBase64(file["url"]).then(base64String => {
			fileData.push({
				"name": file["file"]["name"],
				"content": base64String
			});
		}).catch(error => {
			console.error('Error:', error);
		});
	}
	console.log("FILE DATA")
	console.log(fileData);
	data["files"] = fileData;
	console.log(data);
	// api.post(`/repository/upload/${username}/${repoName}/`, data);
}

export default { uploadFiles }