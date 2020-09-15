package com.zapocet;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Main extends JPanel {
    private static final Color BG_COLOR = new Color(0xFBD0D0);
    private static final String FONT_NAME = "Arial";
    private static final int TILE_SIZE = 64;
    private static final int TILES_MARGIN = 16;

    Field Player1 = new Field();
    Field Player2 = new Field();

    public Main() {
        setPreferredSize(new Dimension(340, 400));
        setFocusable(true);
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
                    resetGame();
                }
                if (!Player1.canMove()) {
                    Player1.myLose = true;
                }
                if (!Player2.canMove()) {
                    Player2.myLose = true;
                }

                if (!Player1.myWin && !Player2.myWin ) {
                    switch (e.getKeyCode()) {
                        case KeyEvent.VK_LEFT:
                            Player2.left();
                            break;
                        case KeyEvent.VK_A:
                            Player1.left();
                            break;
                        case KeyEvent.VK_RIGHT:
                            Player2.right();
                            break;
                        case KeyEvent.VK_D:
                            Player1.right();
                            break;
                        case KeyEvent.VK_DOWN:
                            Player2.down();
                            break;
                        case KeyEvent.VK_S:
                            Player1.down();
                            break;
                        case KeyEvent.VK_UP:
                            Player2.up();
                            break;
                        case KeyEvent.VK_W:
                            Player1.up();
                            break;
                    }
                }

                if (!Player1.myWin && !Player1.canMove()) {
                    Player1.myLose = true;
                }
                if (!Player2.myWin && !Player2.canMove()) {
                    Player2.myLose = true;
                }

                repaint();
            }
        });
        resetGame();
    }

    public void resetGame() {
        Player1.myScore = 0;
        Player1.myWin = false;
        Player1.myLose = false;
        Player1.myTiles = new Tile[4 * 4];
        for (int i = 0; i < Player1.myTiles.length; i++) {
            Player1.myTiles[i] = new Tile();
        }
        Player1.addTile();
        Player1.addTile();

        Player2.myScore = 0;
        Player2.myWin = false;
        Player2.myLose = false;
        Player2.myTiles = new Tile[4 * 4];
        for (int i = 0; i < Player2.myTiles.length; i++) {
            Player2.myTiles[i] = new Tile();
        }
        Player2.addTile();
        Player2.addTile();
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g);
        g.setColor(BG_COLOR);
        g.fillRect(0, 0, this.getSize().width, this.getSize().height);
        g.fillRect(360, 0, this.getSize().width, this.getSize().height);
        for (int y = 0; y < 4; y++) {
            for (int x = 0; x < 4; x++) {
                drawTile(g, Player1.myTiles[x + y * 4], x, y);
                drawTile(g, Player2.myTiles[x + y * 4], x+5, y);
            }
        }

    }

    private void drawTile(Graphics g2, Tile tile, int x, int y) {
        Graphics2D g = ((Graphics2D) g2);
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_NORMALIZE);
        int value = tile.value;
        int xOffset = offsetCoors(x);
        int yOffset = offsetCoors(y);
        g.setColor(tile.getBackground());
        g.fillRoundRect(xOffset, yOffset, TILE_SIZE, TILE_SIZE, 14, 14);
        g.setColor(tile.getForeground());
        final int size = value < 100 ? 36 : value < 1000 ? 32 : 24;
        final Font font = new Font(FONT_NAME, Font.BOLD, size);
        g.setFont(font);

        String s = String.valueOf(value);
        final FontMetrics fm = getFontMetrics(font);

        final int w = fm.stringWidth(s);
        final int h = -(int) fm.getLineMetrics(s, g).getBaselineOffsets()[2];

        if (value != 0)
            g.drawString(s, xOffset + (TILE_SIZE - w) / 2, yOffset + TILE_SIZE - (TILE_SIZE - h) / 2 - 2);

        if (Player1.myWin || Player2.myWin ) {
            g.setColor(new Color(255, 255, 255, 30));
            g.fillRect(0, 0, getWidth(), getHeight());
            g.setColor(new Color(0x87B549));
            g.setFont(new Font(FONT_NAME, Font.BOLD, 48));
            if (Player1.myWin) {
                g.drawString("Player 1 won!", 240, 150);
            }
            if (Player2.myWin) {
                g.drawString("Player 2 won!", 240, 150);
            }
                g.setFont(new Font(FONT_NAME, Font.PLAIN, 16));
                g.setColor(new Color(128, 128, 128, 128));
                g.drawString("Press ESC to play again", 280, getHeight() - 20);

        }
        if ( Player1.myLose || Player2.myLose) {
            g.setColor(new Color(255, 255, 255, 30));
            g.setFont(new Font(FONT_NAME, Font.BOLD, 48));

            if (Player1.myLose) {
                g.setColor(new Color(255, 255, 255, 30));
                g.fillRect(0, 0, 350, getHeight());
                g.setColor(new Color(0x87B549));
                g.setFont(new Font(FONT_NAME, Font.BOLD, 48));
                g.drawString("Game over!", 30, 130);

            }
            if (Player2.myLose) {
                g.setColor(new Color(255, 255, 255, 30));
                g.fillRect(350, 0, getWidth(), getHeight());
                g.setColor(new Color(0x87B549));
                g.setFont(new Font(FONT_NAME, Font.BOLD, 48));
                g.drawString("Game over!", 450, 130);
            }
            if (Player1.myLose && Player2.myLose) {
                g.setColor(new Color(255, 255, 255, 30));
                g.fillRect(0, 0, getWidth(), getHeight());
                g.setColor(new Color(0x87B549));
                g.setFont(new Font(FONT_NAME, Font.BOLD, 48));
                if (Player1.myScore > Player2.myScore) {
                    g.drawString("Player 1 won!", 240, 200);
                }
                else if(Player1.myScore < Player2.myScore)
                {
                    g.drawString("Player 2 won!", 240, 200);
                }
                else
                    g.drawString("Pobedila Druzba", 240, 200);
                //g.drawString("Game over!", 250, 130);
                g.setFont(new Font(FONT_NAME, Font.PLAIN, 16));
                g.setColor(new Color(128, 128, 128, 128));
                g.drawString("Press ESC to play again", 280, getHeight() - 20);
            }
        }
        g.setFont(new Font(FONT_NAME, Font.PLAIN, 18));
        g.drawString("Score: " + Player1.myScore , 16, 345);
        g.drawString("Score: " + Player2.myScore, 418, 345);

    }

    private static int offsetCoors(int arg) {
        return arg * (TILES_MARGIN + TILE_SIZE) + TILES_MARGIN;
    }

    static class Tile {
        int value;

        public Tile() {
            this(0);
        }

        public Tile(int num) {
            value = num;
        }

        public boolean isEmpty() {
            return value == 0;
        }

        public Color getForeground() {
            return value < 16 ? new Color(0x776e65) :  new Color(0xf9f6f2);
        }

        public Color getBackground() {
            switch (value) {
                case 2:    return new Color(0xF6BDB2);
                case 4:    return new Color(0xF0AAB7);
                case 8:    return new Color(0xE78B90);
                case 16:   return new Color(0xFB6767);
                case 32:   return new Color(0xFD7081);
                case 64:   return new Color(0xECA19C);
                case 128:  return new Color(0xedcf72);
                case 256:  return new Color(0xedcc61);
                case 512:  return new Color(0xedc850);
                case 1024: return new Color(0xedc53f);
                case 2048: return new Color(0xedc22e);
            }
            return new Color(0xFCE7E7);
        }
    }
    class Field {
        private Tile[] myTiles;
        boolean myWin = false;
        boolean myLose = false;
        int myScore = 0;


        public void left() {
            boolean needAddTile = false;
            for (int i = 0; i < 4; i++) {
                Tile[] line = getLine(i);
                Tile[] merged = mergeLine(moveLine(line));
                setLine(i, merged);
                if (!needAddTile && !compare(line, merged)) {
                    needAddTile = true;
                }
            }

            if (needAddTile) {
                addTile();
            }
        }

        public void right() {
            myTiles = rotate(180);
            left();
            myTiles = rotate(180);
        }

        public void up() {
            myTiles = rotate(270);
            left();
            myTiles = rotate(90);
        }

        public void down() {
            myTiles = rotate(90);
            left();
            myTiles = rotate(270);
        }

        private Tile tileAt(int x, int y) {
            return myTiles[x + y * 4];
        }

        private void addTile() {
            List<Tile> list = availableSpace();
            if (!availableSpace().isEmpty()) {
                int index = (int) (Math.random() * list.size()) % list.size();
                Tile emptyTime = list.get(index);
                emptyTime.value = Math.random() < 0.9 ? 2 : 4;
            }
        }

        private List<Tile> availableSpace() {
            final List<Tile> list = new ArrayList<Tile>(16);
            for (Tile t : myTiles) {
                if (t.isEmpty()) {
                    list.add(t);
                }
            }
            return list;
        }

        private boolean isFull() {
            return availableSpace().size() == 0;
        }

        boolean canMove() {
            if (!isFull()) {
                return true;
            }
            for (int x = 0; x < 4; x++) {
                for (int y = 0; y < 4; y++) {
                    Tile t = tileAt(x, y);
                    if ((x < 3 && t.value == tileAt(x + 1, y).value)
                            || ((y < 3) && t.value == tileAt(x, y + 1).value)) {
                        return true;
                    }
                }
            }
            return false;
        }

        private boolean compare(Tile[] line1, Tile[] line2) {
            if (line1 == line2) {
                return true;
            } else if (line1.length != line2.length) {
                return false;
            }

            for (int i = 0; i < line1.length; i++) {
                if (line1[i].value != line2[i].value) {
                    return false;
                }
            }
            return true;
        }

        private Tile[] rotate(int angle) {
            Tile[] newTiles = new Tile[4 * 4];
            int offsetX = 3, offsetY = 3;
            if (angle == 90) {
                offsetY = 0;
            } else if (angle == 270) {
                offsetX = 0;
            }

            double rad = Math.toRadians(angle);
            int cos = (int) Math.cos(rad);
            int sin = (int) Math.sin(rad);
            for (int x = 0; x < 4; x++) {
                for (int y = 0; y < 4; y++) {
                    int newX = (x * cos) - (y * sin) + offsetX;
                    int newY = (x * sin) + (y * cos) + offsetY;
                    newTiles[(newX) + (newY) * 4] = tileAt(x, y);
                }
            }
            return newTiles;
        }

        private Tile[] moveLine(Tile[] oldLine) {
            LinkedList<Tile> l = new LinkedList<Tile>();
            for (int i = 0; i < 4; i++) {
                if (!oldLine[i].isEmpty())
                    l.addLast(oldLine[i]);
            }
            if (l.size() == 0) {
                return oldLine;
            } else {
                Tile[] newLine = new Tile[4];
                ensureSize(l, 4);
                for (int i = 0; i < 4; i++) {
                    newLine[i] = l.removeFirst();
                }
                return newLine;
            }
        }

        private Tile[] mergeLine(Tile[] oldLine) {
            LinkedList<Tile> list = new LinkedList<Tile>();
            for (int i = 0; i < 4 && !oldLine[i].isEmpty(); i++) {
                int num = oldLine[i].value;
                if (i < 3 && oldLine[i].value == oldLine[i + 1].value) {
                    num *= 2;
                    myScore += num;
                    int ourTarget = 2048;
                    if (num == ourTarget) {
                        myWin = true;
                    }
                    i++;
                }
                list.add(new Tile(num));
            }
            if (list.size() == 0) {
                return oldLine;
            } else {
                ensureSize(list, 4);
                return list.toArray(new Tile[4]);
            }
        }

        private void ensureSize(java.util.List<Tile> l, int s) {
            while (l.size() != s) {
                l.add(new Tile());
            }
        }

        private Tile[] getLine(int index) {
            Tile[] result = new Tile[4];
            for (int i = 0; i < 4; i++) {
                result[i] = tileAt(i, index);
            }
            return result;
        }

        private void setLine(int index, Tile[] re) {
            System.arraycopy(re, 0, myTiles, index * 4, 4);
        }


    }

    public static void main(String[] args) {
        JFrame game = new JFrame();
        game.setTitle("2048 Game");
        game.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        game.setSize(752, 430);
        game.setResizable(false);

        game.add(new Main());

        game.setLocationRelativeTo(null);
        game.setVisible(true);
    }
}


