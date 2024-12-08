import { useState } from 'react';
import { BACKEND_BASE_URL } from '../config/enviroment';

const useDataPosting = (url) => {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [statusCode , setStatusCode] = useState(null);

  const postData = async (data) => {
    setLoading(true);
    try {
      const isFormData = data instanceof FormData;

      const res = await fetch(`${BACKEND_BASE_URL}/${url}`, {
        method: 'POST',
        headers: isFormData ? undefined : { 'Content-Type': 'application/json' },
        body: isFormData ? data : JSON.stringify(data),
      });
      setStatusCode(res.status)
      const result = await res.json();
      setResponse(result);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return { response, loading, error, postData,statusCode };
};

export default useDataPosting;
