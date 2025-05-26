const express = require('express');
const router = express.Router();
const Event = require('../models/Event');
const auth = require('../middleware/auth');

// Create a new event (admin only)
router.post('/', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    const { title, description, date, time, location } = req.body;

    const event = new Event({
      title,
      description,
      date,
      time,
      location,
      organizer: req.user.userId
    });

    await event.save();
    res.status(201).json(event);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get all events
router.get('/', auth, async (req, res) => {
  try {
    const events = await Event.find()
      .populate('organizer', 'name')
      .sort({ date: 1 });
    res.json(events);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get upcoming events
router.get('/upcoming', auth, async (req, res) => {
  try {
    const events = await Event.find({
      date: { $gte: new Date() },
      status: 'upcoming'
    })
      .populate('organizer', 'name')
      .sort({ date: 1 });
    res.json(events);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get event by ID
router.get('/:id', auth, async (req, res) => {
  try {
    const event = await Event.findById(req.params.id)
      .populate('organizer', 'name')
      .populate('attendees', 'name');
    
    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }
    
    res.json(event);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Update event (admin only)
router.put('/:id', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    const event = await Event.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true }
    );

    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    res.json(event);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Delete event (admin only)
router.delete('/:id', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    const event = await Event.findByIdAndDelete(req.params.id);
    
    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    res.json({ message: 'Event deleted' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Register for event
router.post('/:id/register', auth, async (req, res) => {
  try {
    const event = await Event.findById(req.params.id);
    
    if (!event) {
      return res.status(404).json({ message: 'Event not found' });
    }

    if (event.attendees.includes(req.user.userId)) {
      return res.status(400).json({ message: 'Already registered for this event' });
    }

    event.attendees.push(req.user.userId);
    await event.save();

    res.json(event);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router; 