# runningmax
Get runningmax for last N entries from a stream of random ints

## Test setup
A local installation of RabbitMQ was setup to run on <code>localhost</code>, port <code>5672</code>.

Three scripts were then implemented in Python to serve as a 'replica' of the actual test:

<ul>
  <li><code>rng_pub.py</code> - publishes JSON-formatted messages containing fields:
    <ul>
        <li>rand - int</li>
        <li>sequence_number - int</li>
    </ul>
  </li>
  <li><code>max_pubsub.py</code></li>
  <li><code>end_sub.py</code></li>
</ul>

### RNG publisher
An integer( _rand_ ) between (0,1000) is created, along with a _sequence\_number_ . A simple for-loop runs N=10000 times, creating messages on the following format:

```
message = {
    "sequence_number" : int(i),
    "rand" : int(make_rng())
}
```

The message _dict_ is published as JSON (json.dumps()).

### Running Max subscriber/publisher
