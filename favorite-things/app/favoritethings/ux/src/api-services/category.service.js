import axios from './init';

const RESOURCE_NAME = '/category';

export default (config) => {
  return {
    getAll() {
      return axios.get(RESOURCE_NAME, config);
    },

    get(id) {
      return axios.get(`${RESOURCE_NAME}/${id}`, config);
    },

    create(data) {
      return axios.post(RESOURCE_NAME, data, config);
    },

    update(id, data) {
      return axios.put(`${RESOURCE_NAME}/${id}`, data, config);
    },

    newThing(id, data) {
      return axios.put(`${RESOURCE_NAME}/${id}`, data, config);
    },

    delete(id) {
      return axios.delete(`${RESOURCE_NAME}/${id}`, config);
    }
  };
};
