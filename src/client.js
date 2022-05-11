import config from "./config"
const axios = require("axios")  // 1


class FastAPIClient {
	constructor(overrides) {
		this.config = {
			...config,
			...overrides,
		}

		this.apiClient = this.getApiClient(this.config)  // 2
	}

	/* Create Axios client instance pointing at the REST api backend */
	getApiClient(config) {
		let initialConfig = {
			baseURL: `${config.apiBasePath}`,  // 3
		}
		let client = axios.create(initialConfig)
		return client
	}

	getPrediction(msg) {
		return this.apiClient.post(`/predict?msg=${msg}`).then(({data}) => {  // 5
			return data
		})
	}
}
export default FastAPIClient;