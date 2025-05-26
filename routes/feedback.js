const express = require('express');
const router = express.Router();
const Feedback = require('../models/Feedback');
const auth = require('../middleware/auth');

// Submit feedback
router.post('/', auth, async (req, res) => {
  try {
    const { eventId, rating, comment, mood } = req.body;

    const feedback = new Feedback({
      user: req.user.userId,
      event: eventId,
      rating,
      comment,
      mood
    });

    await feedback.save();

    res.status(201).json(feedback);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get feedback for a specific event
router.get('/event/:eventId', auth, async (req, res) => {
  try {
    const feedback = await Feedback.find({ event: req.params.eventId })
      .populate('user', 'name')
      .sort({ createdAt: -1 });

    res.json(feedback);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get user's feedback
router.get('/my-feedback', auth, async (req, res) => {
  try {
    const feedback = await Feedback.find({ user: req.user.userId })
      .populate('event', 'title date')
      .sort({ createdAt: -1 });

    res.json(feedback);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get all feedback (admin only)
router.get('/all', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    const feedback = await Feedback.find()
      .populate('user', 'name')
      .populate('event', 'title')
      .sort({ createdAt: -1 });

    res.json(feedback);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router; 