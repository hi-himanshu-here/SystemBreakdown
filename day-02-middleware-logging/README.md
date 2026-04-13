## 🧠 Concepts Learned

### Middleware
Middleware acts as an interceptor between request and response.

### Logging
Tracks incoming requests and outgoing responses with timing.

### Error Handling
Centralized error handling ensures system stability.

---

## ⚙️ Request Lifecycle

Client → Middleware → View → Middleware → Response

---

## ⚠️ Scaling Considerations

- Logging should be centralized
- Avoid excessive logging
- Use structured logs in production

---

## 🚀 Future Improvements

- Integrate logging tools (ELK, Datadog)
- Add request tracing
- Add rate limiting middleware

## 🚦 Rate Limiting

Implemented a custom rate limiting middleware to restrict the number of requests per client.

### Approach
- Sliding window algorithm
- Tracks requests per IP
- Limits to 5 requests per minute

### Limitations
- In-memory storage (not scalable)
- Not suitable for distributed systems
- No user-based tracking

### Real-world Solutions
- Redis-based rate limiting
- Token bucket algorithm
- API gateway enforcement